# Create your views here.
import datetime, sys
from django.template import Context, loader
from django.template import RequestContext
from django.shortcuts import render_to_response, get_object_or_404
from django.http import HttpResponseRedirect
from django.http import HttpResponse
from django.http import Http404
from clwmail.mail_auth.sql.viewdb import AuthModel 
from clwmail.mail_auth.forms import LoginForm 

from clwmail import settings

urlrel = settings.RELATIVE_URL
status_mapper = settings.STATUS_MAPPER

thistemplate = 'base.html'

# Create your views here.
class AuthUser (object):
	''' A light weight user object which
		is stored as in the session.'''

	def __init__(self, user_id, domain, status, b_isadmin):

		self.username = user_id
		self.domain = domain 
		self.status = status 
		self.b_isadmin = b_isadmin 

	# If we are we ar authenticated
	def is_authenticated(self):
		return True

def login(request):
	''' This method provides a mechanism for users
		to log into the system. If credentials are
		correctly supplied the user will be set
		as the session user. Othewise, the view
		is rendered anew with appropriate error messages'''

	# Create model instance	
	model = AuthModel()
	# The object which will contain
	# the current session user, if one exists
	user = None
	# The error to be displayed if form validates
	# but credentials are incorrect
	error = None
	#Default data if no post
	new_data = None
	form = LoginForm()
	# If a user is already logged in, then redirect
	# to the appropirate holiday page.
	if request.session['user'].is_authenticated():
			user = request.session['user']
			if user.b_isadmin:
				return HttpResponseRedirect(urlrel + 'admin/user/manage/' )

			else:
				return HttpResponseRedirect(urlrel +
					'mailstore/user/%s/domain/%s/holiday/' % (user.username, user.domain)) 

	# Otherwise go to login page
	else:
		# Check if we are validating post information
		if request.method == "POST" and "username" in request.POST:
			# Get post information
			new_data = request.POST.copy()
			# Bind form to post data
			form = LoginForm(new_data)
			if form.is_valid():
				# Get cleaned data. This a standardized
				# output for a range of given input
				cleaned_data = form.clean()
				username = str(cleaned_data['username'])
				password = str(cleaned_data['password'])
				user = model.login(username,password)
				if not model.error and not user.userid:
					# If user doesnt exist, then supplied crendentials are incorrect
					error = "Your username and password combination was not found"		

				else:
					# If the user was found check he/she is active
					try:
						string_status =	status_mapper[user.status]
					except KeyError:
							# if the status is not found default to not active. 
							error = "Your account is not active. Please contact Rory Campbell-Lange."		
					else:
						# We have found a valid status. Check its active
						if status_mapper[user.status] == "Inactive":
							# If user status is inactive
							error = "Your account is not active. Please contact Rory Campbell-Lange."		
						else:
							# If user does exist, then we assign them as current session user
							session_user =  AuthUser(user.userid, 
													 user.domain,
													 user.status,
													 user.b_isadmin) 
							request.session['user'] = session_user
							# Get the request url to redirect to 
							# This is the url the user wanted to go to before logging in.
							redirect_url = request.session.get('pre_auth_url', None)
							if redirect_url:
								# Remove the request url as it is no longer needed.
								del request.session['pre_auth_url']
								return HttpResponseRedirect(redirect_url)

							else:
								if session_user.b_isadmin:
									# redirect to management page 
									return HttpResponseRedirect(urlrel + 'admin/user/manage/')

								else:
									# otherwise Redirect to user home page
									return HttpResponseRedirect(urlrel + 'mailstore/user/%s/domain/%s/holiday/' % 
																							(session_user.username,
																							 session_user.domain))

		return render_to_response('auth/login.html',
				{'thistemplate':thistemplate,
				'form':form, 
				'new_data':new_data,
				'loginerror':error},
				context_instance=RequestContext(request))
					
def deny(request,item):
	return render_to_response('auth/deny.html',
			{'item':item, 'thistemplate':thistemplate },
			context_instance=RequestContext(request))

def logout(request):
	''' This method provides a mechanism for users
		to logout of the system. This method simply 
		deletes the current user from the session.
		'''
	# check to ensure a user is currently logged-in 
	try:
		user = request.session['user']
	except KeyError:
	# if not, then dont do anything
		pass
	# otherwise, remove user from session.
	else:
		del request.session['user']
		for key in request.session.keys():
			del request.session[key]

	# Redirect to login page.
	return HttpResponseRedirect(urlrel + 'auth/login/')

