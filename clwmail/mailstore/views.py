# Create your views here.
import sys
from django.template import Context, loader
from django.template import RequestContext
from django.shortcuts import render_to_response, get_object_or_404
from django.http import HttpResponseRedirect
from django.http import HttpResponse
from django.http import Http404
from clwmail.mail_auth.decorators import must_login 
from clwmail.mail_auth.permissions import canview 
from clwmail.mailstore.sql.viewdb import MailModel
from clwmail.mailstore.forms import HolidayForm 

from clwmail import settings
from datetime import datetime

urlrel = settings.RELATIVE_URL
calurl = settings.CALENDAR_URL

status_mapper = settings.STATUS_MAPPER

thistemplate = 'base.html'

@must_login
def holiday(request, username=None, domain=None):
	''' 
		A simple wrapper method around the responder 
	'''

	if canview(request, username, domain):
		return _holidayresponder(request, username, domain)

	else:
		return HttpResponseRedirect(urlrel + 'auth/deny/profile/')

@must_login
def _holidayresponder(request, username, domain, adict={}):
	''' 
		This method manages a users holiday.  It ensures the session user is
		logged in.  It retrieves a detailed view of the user including username
		and status. Also, it retrieves the user's holiday messages, and if the
		user is currently set to Holiday, retrieves the current holiday
		message.
	'''

	if not canview(request, username, domain):
		return HttpResponseRedirect(urlrel + 'auth/deny/profile/')

	# Instantiate model
	model = MailModel()
	# Set the default mode. This may get overwritten by the paramater dict
	mode ='add'
	# Get all the required details for this user
	detailed_user = model.getuserdetails(username, domain)
	#Get all of this person's holiday messages
	holiday_messages = model.getuserholidays(username, domain)
	# The current holiday if the status is holiday
	current_holiday = None
	if status_mapper[detailed_user.status] == "Holiday":
		#Get this person's current holiday messages
		current_holiday = model.getcurrentholiday(username, domain)

	defaultmsg = detailed_user.default_message

	info_dict =  {'thistemplate':thistemplate,
				  'detailed_user': detailed_user,
				  'holiday_messages': holiday_messages,
				  'current_holiday': current_holiday,
				  'defaultmsg': defaultmsg,
				  'current_page': 'holiday',
				  'calurl': calurl,
				  'mode': mode}

	info_dict.update(adict)

	return render_to_response('mailstore/holiday.html',
							  info_dict,
							  context_instance=RequestContext(request))
@must_login
def holidayadd(request, username, domain):
	''' 
		This methos allows a user to add a holiday message It requires the data
		to be posted and all data to be validated. Upon succesfull completion
		of the message form, the user is redirected to the same holiday
		management page with the new holiday message appearing in the list of
		holidays. If an error has occured the holiday responder is called in
		order to show the errors 
	'''

	if not canview(request, username, domain):
		return HttpResponseRedirect(urlrel + 'auth/deny/profile/')

	# Instantiate model
	model = MailModel()
	# Mode set
	mode = "add"
	# Ensure we have posted data
	if request.method =="POST":
		# create a copy of the post data
		# so we are not directly manipulating it
		new_data = request.POST.copy()
		# Create a concat version of the different fields
		# for the startdate
		new_data['hstart_date'] = _datemaker(new_data['hs_day'],
											 new_data['hs_month'],
											 new_data['hs_year'],
											 new_data['hs_hour'],
											 new_data['hs_min'])
		# Create a concat version of the different fields
		# for the end date 
		new_data['hend_date'] = _datemaker(new_data['he_day'],
										   new_data['he_month'],
										   new_data['he_year'],
										   new_data['he_hour'],
										   new_data['he_min'])
		# Bind form to post data
		form = HolidayForm (new_data)
		# Check if form is valid
		if form.is_valid():
			# Standardized data
			cleaned_data = form.clean()	
		 	param_dict = {'mode':1,
						  'username':username,
						  'domain':domain,
						  'hstart':cleaned_data['hstart_date'],
						  'hend':cleaned_data['hend_date'],
						  'message':cleaned_data['message'],
						  'id':-1,
						  'b_default':cleaned_data['b_default']}
			
			result = model.manageholiday(**param_dict)
			if not result and model.error:
				errors = {'form':form, 'new_data':new_data, 
						  'mode':mode, 'dberror':model.error }
				return _holidayresponder(request, username, domain, adict=errors)
				
		# If not valid call responder with error
		else:
			errors = {'form':form,'new_data':new_data, 'mode':mode}
			return _holidayresponder(request, username, domain,  adict=errors)

	return HttpResponseRedirect(urlrel + "mailstore/user/%s/domain/%s/holiday/" %
															(username, domain))

@must_login
def holidaydelete(request, username, domain, hol_id):
	''' 
		This method allows a user to delete a holiday message from the queue
		succesfull deletion of the message redirects the user to the same
		holiday management page with message deleted.  If an error has occured
		the holiday responder is called in order to show the errors 
	'''

	if not canview(request, username, domain):
		return HttpResponseRedirect(urlrel + 'auth/deny/profile/')

	# Instantiate model
	model = MailModel()
	# Set up for delete
	param_dict = {'mode':3,
				  'username':username,
				  'domain':domain,
				  'hstart':None,
				  'hend':None,
				  'message':None,
				  'id':int(hol_id),
				  'b_default': None}
				
	result = model.manageholiday(**param_dict)

	if not result and model.error:
		errors = {'dberror':model.error }
		return _holidayresponder(request, username, domain, adict=errors)

	return HttpResponseRedirect(urlrel + "mailstore/user/%s/domain/%s/holiday/" % 
																	(username,domain))

@must_login
def holidayedit(request, username, domain, hol_id):
	''' 
		This method allows a user to edit a holiday message from the queue.
		succesfull update of the message redirects the user to the same holiday
		management page .  If an error has occured the holiday responder is
		called in order to show the errors 
	'''

	# Ensure the user can view this.
	if not canview(request, username, domain):
		return HttpResponseRedirect(urlrel + 'auth/deny/profile/')
	
	model = MailModel()
	# Set the mode
	mode = "edit"
	# Get the requested holiday
	holiday = model.getholiday(int(hol_id), username, domain)	
	# If the holiday was not found
	if (holiday and not holiday.holid):
		raise Http404

	if request.method =="POST" :
		# create a copy of the post data
		# so we are not directly manipulating it
		new_data = request.POST.copy()
		# Create a concat version of the different fields
		# for the startdate
		new_data['hstart_date'] = _datemaker(new_data['hs_day'],
											 new_data['hs_month'],
											 new_data['hs_year'],
											 new_data['hs_hour'],
											 new_data['hs_min'])
		# Create a concat version of the different fields
		# for the end date 
		new_data['hend_date'] = _datemaker(new_data['he_day'],
										   new_data['he_month'],
										   new_data['he_year'],
										   new_data['he_hour'],
										   new_data['he_min'])
		# Bind form to post data
		form = HolidayForm (new_data)

		# Check if form is valid
		if form.is_valid():
			# Standardized data
			cleaned_data = form.clean()	
			# Set up for edit
		 	param_dict = {'mode':2,
						  'username':username,
						  'domain':domain,
						  'hstart':cleaned_data['hstart_date'],
						  'hend':cleaned_data['hend_date'],
						  'message':cleaned_data['message'],
						  'id':holiday.holid,
						  'b_default':cleaned_data['b_default']}
			
			# Manage the holiday
			result = model.manageholiday(**param_dict)

			# Ensure no errors have occured
			if not result and model.error:
				errors = {'form':form, 'new_data':new_data, 
						  'mode':mode, 'dberror':model.error,
						  'holiday':holiday }
				return _holidayresponder(request, username, domain, adict=errors)
			
			return HttpResponseRedirect(urlrel + "mailstore/user/%s/domain/%s/holiday/" % 
																		(username, domain))

		# If not valid call responder with error
		else:
			errors = {'form':form,'new_data':new_data, 'holiday':holiday, 'mode':mode}
			return _holidayresponder(request, username, domain, errors)

	return _holidayresponder(request, username, domain, adict={'mode':mode,'holiday':holiday})

@must_login
def leaveoff(request, username, domain):
	''' 
		This method changes the status of the requested user to 1 (active),
		removing the leave message display seen by the user.
	''' 

	if not canview(request, username, domain):
		return HttpResponseRedirect(urlrel + 'auth/deny/profile/')
	
	model = MailModel()
	# Set parameters
	param_dict = {'mode':2,
				  'username':username,
				  'domain':domain,
				  'hstart':None,
				  'hend':None,
				  'message':None,
				  'id':None}
	# execute query
	result = model.removeleave(**param_dict)
	# Return to holiday page.
	return HttpResponseRedirect(urlrel + "mailstore/user/%s/domain/%s/holiday/" % 
																(username,domain))
	

###################################################################
######################### Helper Methods ########################## 
###################################################################

def _datemaker(day, month, year, hour, min):
	''' THis method takes all the parameters
		and creates a unified string '''

	fulldate = "%s-%s-%s %s:%s:00" % (year, month, day, hour, min)
	return fulldate
