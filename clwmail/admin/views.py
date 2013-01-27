import string
from random import choice
from datetime import datetime
from django.template import RequestContext
from django.shortcuts import render_to_response
from django.shortcuts import get_object_or_404
from django.http import HttpResponseRedirect
from django.http import HttpResponse
from django.http import Http404
from clwmail.mail_auth.decorators import mustbe_admin
from clwmail.admin.sql.viewdb import AdminModel 
from clwmail.admin.forms import UserAdd
from clwmail.admin.forms import UserEdit
from clwmail.admin.forms import DomainAdd
from clwmail.admin.forms import DomainEdit
from clwmail.admin.forms import GroupAdd
from clwmail.admin.forms import GroupEdit
from clwmail import settings
from utilities.pagination import  paginatorwrapper
from utilities.format import removewhitespace 

thistemplate = 'admin/admingen.html'

urlrel 			= settings.RELATIVE_URL
status_mapper 	= settings.STATUS_MAPPER
mailstore_home	= settings.MAILSTORE_HOME
types 			= settings.TYPERS
user_uid 		= settings.UID
user_gid 		= settings.GID
items_per_page 	= settings.ITEMS_PER_PAGE

@mustbe_admin
def usermanage(request, page_num=None):
	'''
		This view is simply a wrapper around the user manage responder.
	'''
	return _usermanageresponder (request, page_num)

@mustbe_admin
def _usermanageresponder(request, page_num=None, adict={}):
	''' 
		This method provides a mechanism for and admin user to mange people.
		The decorator ensures that the user is an admin before proceeding. The
		page lists a paginated view of current users.  add allows the admin to
		add more users
	'''
	
	# Create model instance
	model = AdminModel()
	# default mode
	mode ='add'
	# Get all the users in the 
	# system that are not admins
	users = list(model.getallusers())
	# Set page based on passed in number or session
	page = page_num or request.session.get('u_page',1)
	# Set the page number in the session
	request.session['u_page'] = page
	# Defaults
	ucollection, users_page = paginatorwrapper(users, page, per_page=items_per_page, orphans=1)
	# Get all available domains
	domains = list(model.getalldomains())
	# Generate a password
	generated_pass = _gen_pass()

	# The template vars
	info_dict = {'users':users_page,
				 'collection': ucollection,
				 'domains':domains,
				 'page':'umanage',
				 'gen_pass':generated_pass,
				 'mode':mode,
				 'types':types,
				 'thistemplate':thistemplate}

	# update the template vars
	info_dict.update(adict)

	return render_to_response('admin/usermanage.html', info_dict,
							   context_instance=RequestContext(request))

@mustbe_admin
def useradd(request):
	''' 
		This method adds a user into the system. It awaits posted data from the
		user, validates said data, and if and error occurs uses the responder
		to display them to the user. A succesfull post will create the user
		using the viewdb function and redirect to avoid post problems 
	'''

	# Create model instance
	model = AdminModel()
	# Set the mode
	mode ="add"
	# Check we have posted data
	if request.method == "POST":
		# copy posted data
		new_data = request.POST.copy()
		# Strip strings of leading/preceding whitespace
		removewhitespace(new_data)
		# bind form instance
		form = UserAdd(new_data)
		# Ensure for is valid
		if form.is_valid():
			# Standardized data
			cleaned_data = form.cleaned_data
			# Create the parameters
			params = {'mode': 1,
					  'userid': cleaned_data['userid'],
					  'password': cleaned_data['password'],
					  'home': mailstore_home % cleaned_data['userid'],
					  'domain': cleaned_data['domain'],
					  'uid': user_uid,
					  'gid': user_gid,
					  'status': 1,
					  'typer': cleaned_data['typer'].capitalize(),
					  'role': cleaned_data['role'],	
					  'fullname': cleaned_data['fullname'],
					  'notes': cleaned_data['notes']
					  }
			# add the user
			useradded = model.manageuser(params)
			# Ensure there was no error
			if not useradded or model.error:
				# If there was an error, display it to the user
				errors = {'form':form, 'new_data':new_data, 
						  'mode':mode, 'dberror':model.error}
				# Use the responder to show.
				return _usermanageresponder(request, adict=errors)

		# If not valid call responder with error
		else:
			# This gets rendered if the form entries were incorrect
			errors = {'form':form, 'new_data':new_data, 'mode':mode}
			return _usermanageresponder(request, adict=errors)
			
	return HttpResponseRedirect (urlrel + 'admin/user/manage/')

@mustbe_admin
def useredit(request, userid, domain):
	''' 
		This method edits an existing user of the system. it fills the form
		with the users details and then awaits posted data from the user,
		validates said data, and if and error occurs uses the responder to
		display them to the user. A succesfull post will update the user using
		the viewdb function and redirect to avoid post problems 
	'''

	# Create model instance
	model = AdminModel()
	# Set the mode
	mode ="edit"
	# Retrieve the requested user.
 	request_user =  model.getuser(userid, domain)
	# If there was no user in the db with this name or the function has thrown
	# an error, we have been given bogus input data
	if (request_user and not request_user.userid) or (not request_user and model.error):
		# Raise user has not be found
		raise Http404

	# Check we have posted data
	if request.method =="POST":
		# copy posted data
		new_data = request.POST.copy()
		# Remove white space.
		removewhitespace(new_data)
		# bind form instance
		form = UserEdit(new_data)
		# Ensure for is valid
		if form.is_valid():
			# Clean the data
			cleaned_data = form.cleaned_data
			# create function parameter list
			params = {'mode': 2, # edit
					  'userid': cleaned_data['userid'],
					  'password': cleaned_data['password'],
					  'home': mailstore_home % cleaned_data['userid'],
					  'domain': cleaned_data['domain'],
					  'uid': user_uid,
					  'gid': user_gid,
					  'status': 1,
					  'typer': cleaned_data['typer'].capitalize(),
					  'role': cleaned_data['role'],	
					  'fullname': cleaned_data['fullname'],
					  'notes': cleaned_data['notes']}
			# call manageuser in edit mode
			useredited = model.manageuser(params)

			# Ensure no errors have occured
			if not useredited and model.error:
				# if we have errors display them
				errors = {'form':form, 'new_data':new_data,
						  'requestuser':request_user, 'mode':mode,
						   'dberror':model.error}
				# Use the responder
				return _usermanageresponder(request, adict=errors)

			# Redirect to avoid post problems
			return HttpResponseRedirect (urlrel + 'admin/user/manage/')

		# If not valid call responder with error
		else:
			errors = {'form':form, 'new_data':new_data, 
					  'mode':mode, 'requestuser':request_user}
			return _usermanageresponder(request, adict=errors)
		
	return _usermanageresponder(request, adict={'requestuser':request_user, 
												 'mode':mode})
@mustbe_admin
def userhide(request, userid, domain):
	''' 
		This method hides a user from the system by setting said user's status
		equal to 9. This will ensure that this person can no longer log in to
		the system.
	'''
		
	# Create model instance
	model = AdminModel()
	# Retrieve the requested user.
	request_user = model.getuser(userid, domain)

	# If there was no user in the db with this name or the function has thrown
	# an error, we have been given bogus input data
	if (request_user and not request_user.userid) or (not request_user and model.error):
		# Raise user has not be found
		raise Http404
	
	# First remove user from aliases that point to him/her All previously
	# selected users
	params = {'mode':4, # remove alias users
			  'alias':None,
			  'userid':request_user.userid,
			  'domain':request_user.domain
			 }

	# Remove user from aliases
	aliasuserdeleted = model.managealiasuser(params)
	# Ensure no errors have occured
	if not aliasuserdeleted and model.error:
		# Make new template context
		errors = {'mode':'add', 'requestuser':request_user,
				 'hideerror':model.error}
		# use responder to show errors
		return _usermanageresponder(request, adict=errors)

	# Set up for hidding user 
	params = {'mode': 4,
			  'userid': request_user.userid,
			  'password': None,
			  'home': None,
			  'domain': request_user.domain,
			  'uid': None,
			  'gid': None,
			  'status': 9,
			  'typer': None,
			  'role': None,	
			  'fullname': None,
			  'notes':None 
			  }

	# Hide user
	userhidden = model.manageuser(params)
	# Show errors if occured
	if not userhidden and model.error:
		# Create new template context
		errors = {'mode':'add', 'requestuser':request_user,
				  'hideerror':model.error }
		# User responder to show errors
		return _usermanageresponder(request, adict=errors)

	return HttpResponseRedirect (urlrel + 'admin/user/manage/')

@mustbe_admin
def userunhide(request, userid, domain):
	''' 
		This method un-hides a user from the system by setting said user's
		status equal to 1. This will ensure that this person can login to the
		system.
	'''
		
	# Create model instance
	model = AdminModel()
	# Retrieve the requested user.
	request_user =  model.getuser(userid, domain)

	# If there was no user in the db with this name or the function has thrown
	# an error, we have been given bogus input data
	if (request_user and not request_user.userid) or (not request_user and model.error):
		# Raise user has not be found
		raise Http404
	
	# Set up for unhide
	params = {'mode': 5,
			  'userid': request_user.userid,
			  'password': None,
			  'home': None,
			  'domain': request_user.domain,
			  'uid': None,
			  'gid': None,
			  'status': 1,
			  'typer': None,
			  'role': None,	
			  'fullname': None,
			  'notes':None 
			  }
	#re-enable user
	userunhidden = model.manageuser(params)

	# Make sure no errors have occured.
	if not userunhidden and model.error:
		errors = {'mode':'add', 'requestuser':request_user }
		return _usermanageresponder(request, adict=errors)

	return HttpResponseRedirect (urlrel + 'admin/user/manage/')
		
@mustbe_admin
def genpass(request):
	'''
		This method is a wrapper around _gen_pass() and is called, via ajax,
		when the user wants to regenerate a password.
	'''
	# Generate a new password
	password = _gen_pass()

	# Respond with password
	return HttpResponse(password)

@mustbe_admin
def domainmanage(request, page_num=None):
	'''
		This view simply a wrapper around the domainmanager.
	'''

	return _domainmanageresponder (request, page_num)

@mustbe_admin
def _domainmanageresponder(request, page_num=None, adict={}):

	''' 
		This method provides a mechanism for and admin user to manage domains.
		The decorator ensures that the user is an admin before proceeding. The
		page lists a paginated view of current domains.  add allows the admin
		to add more domains
	'''

	# Create model instance
	model = AdminModel()
	# default mode
	mode ='add'
	# Get all the domains in the 
	# system that are not admins
	domains = list(model.getalldomains())
	# Set page based on passed in number or session
	page = page_num or request.session.get('d_page',1)
	# Set the page number in the session
	request.session['d_page'] = page
	# Get collection and current page
	dcollection, domains_page = paginatorwrapper(domains, page, per_page=items_per_page, orphans=1)

	# The template vars
	info_dict = {'domains':domains_page,
				 'collection': dcollection,
				 'page':'dmanage',
				 'mode':mode,
				 'thistemplate':thistemplate}
	# update the template vars
	info_dict.update(adict)

	return render_to_response('admin/domainmanage.html',
							  info_dict,
							  context_instance=RequestContext(request))


@mustbe_admin
def domainadd(request):
	''' 
		This method adds a domain into the system. It awaits posted data from
		the user, validates said data, and if and error occurs uses the
		responder to display them to the user. A succesfull post will create
		the domain using the viewdb function and redirect to avoid post
		problems 
	'''

	# Create model instance
	model = AdminModel()
	# Set the mode
	mode ="add"
	# Check we have posted data
	if request.method =="POST":
		# copy posted data
		new_data = request.POST.copy()
		# Remove white space
		removewhitespace(new_data)
		#  bind form instance
		form = DomainAdd(new_data)

		# Ensure for is valid
		if form.is_valid():
			# Get standardized data
			cleaned_data = form.cleaned_data
			# Set up for add mode.
			params = {'mode': 1,
					  'domainname': cleaned_data['domain'],
					  'newdomainname': None,
					  }
			# Add domain
			domainadded = model.managedomain(params)

			# Make sure no errors occured.
			if not domainadded and model.error:
				errors = {'form':form, 'new_data':new_data, 
						  'mode':mode, 'dberror':model.error }
				return _domainmanageresponder(request, adict=errors)

		# If not valid call responder with error
		else:
			errors = {'form':form,'new_data':new_data, 'mode':mode}
			return _domainmanageresponder(request, adict=errors)
			
	return HttpResponseRedirect (urlrel + 'admin/domain/manage/')

@mustbe_admin
def domainedit(request, domain_name):
	''' 
		This method edits an existing domain of the system. it fills the form
		with the domain details and then awaits posted data from the user,
		validates said data, and if and error occurs uses the responder to
		display them to the user. A succesfull post will update the domain
		using the viewdb function and redirect to avoid post problems 
	'''

	# Create model instance
	model = AdminModel()
	# Set the mode
	mode ="edit"
	# Retrieve the requested user.
 	request_domain =  model.getdomain( domain_name)
	# If there was no user in the db with this name or 
	# the function has thrown an error, we have been 
	# given bogus input data
	if (request_domain and not request_domain.domainname) or (not request_domain and model.error):
		# Raise user has not be found
		raise Http404

	# Check we have posted data
	if request.method =="POST":
		# copy posted data
		new_data = request.POST.copy()
		# remove whitespaces
		removewhitespace(new_data)
		# bind form instance
		form = DomainEdit(request_domain.domainname, kargs=new_data)
		# Ensure for is valid
		if form.is_valid():
			# Clean the data
			cleaned_data = form.cleaned_data
			# create function parameter list
			params = {'mode': 2, # edit
					  'domainname': request_domain.domainname,
					  'newdomainname': cleaned_data['domain']}
			# call managedomain in edit mode
			domainedited = model.managedomain(params)
			# Ensure no errors have occured
			if not domainedited and model.error:
				# if we have errors display them
				errors = {'form':form, 'new_data':new_data,
						  'requestdomain':request_domain, 'mode':mode,
						   'dberror':model.error}
				# Use the responder
				return _usermanageresponder(request, adict=errors)
			# Redirect to avoid post problems
			return HttpResponseRedirect (urlrel + 'admin/domain/manage/')

		# If not valid call responder with error
		else:
			errors = {'form':form, 'new_data':new_data, 
					  'mode':mode, 'requestdomain':request_domain}
			return _domainmanageresponder(request, adict=errors)
			
	return _domainmanageresponder(request, adict={'requestdomain':request_domain, 
												 'mode':mode})
	

@mustbe_admin
def domaindelete(request, domain_name):
	''' 
		This method deletes an existing domain of the system. This can only
		occur if not people are referencing the domain. If the domain is being
		referenced the user can not delete the domain
	'''

	# Create model instance
	model = AdminModel()
	# Set the mode
	mode ="add"
	# Retrieve the requested domain.
 	request_domain =  model.getdomain(domain_name)
	# If there was no domain in the db with this name or the function has
	# thrown an error, we have been given bogus input data
	if (request_domain and not request_domain.domainname) or (not request_domain and model.error):
		# Raise domain has not be found
		raise Http404

	# Set up for delete
	params = {'mode': 3,
			  'domainname': request_domain.domainname,
			  'newdomainname':None,
			  }

	# Delete domain
	domaindeleted = model.managedomain(params)

	# Ensure no errors have occured
	if not domaindeleted and model.error:
		errors = {'requestdomain':request_domain, 'mode':mode,
				   'deleteerror':model.error }
		
		return _domainmanageresponder(request, adict=errors)

	# Redirect to avoid post problems
	return HttpResponseRedirect (urlrel + 'admin/domain/manage/')

@mustbe_admin
def groupmanage(request, page_num=None):
	'''
		This method simply calls the group manage responder.
	'''
	return _groupmanageresponder (request, page_num)

@mustbe_admin
def _groupmanageresponder(request, page_num=None, adict={}):
	''' 
		This method provides a mechanism for and admin user to mange groups.
		The decorator ensures that the user is an admin before proceeding. The
		page lists a paginated view of current groups.  add allows the admin to
		add more groups
	'''

	# Create model instance
	model = AdminModel()
	# default mode
	mode ='add'
	# Get all the aliases in the 
	# system that are not admins
	aliases = list(model.getallaliases() or [])
	# Set page based on passed in number or session
	page = page_num or request.session.get('a_page',1)
	# Set the page number in the session
	request.session['a_page'] = page
	# Get collection and current page
	acollection, aliases_page = paginatorwrapper(aliases, page, per_page=items_per_page, orphans=1)
	# Get all available domains
	domains = list(model.getalldomains())

	# The template vars
	info_dict = {'aliases':aliases_page,
				 'collection': acollection,
				 'domains': domains,
				 'page':'gmanage',
				 'mode':mode,
				 'is_domain':True,
				 'thistemplate':thistemplate}

	# update the template vars
	info_dict.update(adict)

	return render_to_response('admin/groupmanage.html', info_dict,
							  context_instance=RequestContext(request))

@mustbe_admin
def getaliasusers(request, domain_name):
	''' 
		This method gets all the users associated to particular domain. It is
		used as an ajax call on the group management page. There reason for
		this is that only users of the domain associated to the alias can be
		selected. This is is not known ahead of time and is hence done
		dynamically.
	'''

	# Make model instance
	model = AdminModel()
	# Get the domain to see if it is valid
	domain = model.getdomain(domain_name)
	# Is it a valid domain
	is_domain = False
	# Check valid domain
	if domain and domain.domainname and not model.error:
		is_domain = True

	domain_users = DomainUsers(domain_name, model.getnondisabledusers(domain_name))
	# Default new_data values
	new_data = None

	if request.method == "POST":
		new_data = request.POST.copy()
		try:
			users_string = new_data['users']
		except KeyError:
			new_data = None	
		else:
			new_data.update({'users':users_string.split(',')})

	return render_to_response('admin/aliasusers.html',
							  {'domain_users':domain_users,
							   'new_data':new_data,
							   'is_domain':is_domain},
							  context_instance=RequestContext(request))
@mustbe_admin
def groupadd(request):
	''' 
		This method adds a group into the system. It awaits posted data from
		the user, validates said data, and if and error occurs uses the
		responder to display them to the user. A succesfull post will create
		the group using the viewdb function and redirect to avoid post problems 
	'''

	# Create model instance
	model = AdminModel()
	# Set the mode
	mode ="add"
	# Check we have posted data
	if request.method =="POST":
		# copy posted data
		new_data = request.POST.copy()
		# The selected users
		users = [str(user) for user in request.POST.getlist('users')]
		# Update the post dict
		new_data.update({'users':users})
		# remove white spaces
		removewhitespace(new_data)
		# bind form instance
		form = GroupAdd(kargs=new_data)

		# Ensure for is valid
		if form.is_valid():
			# get standardized data
			cleaned_data = form.cleaned_data
			# Set up for add mode 
			params = {'mode': 1,
					  'alias': cleaned_data['alias'],
					  'domain': cleaned_data['domain'],
					  'new_alias': None,
					  'notes': cleaned_data['notes']
					  }
			# Add alias
			aliasadded = model.managealias(params)
			# Ensure not errors have occured
			if not aliasadded and model.error:
				# Create a new template context
				errors = {'form':form, 'new_data':new_data, 
						  'mode':mode, 'dberror':model.error }

				# User responder to show errors
				return _groupmanageresponder(request, adict=errors)

			# Once the alias has been created, we add the selected users
			for user in users:
				# Split the string of usernames These need to be usernames as
				# that is the only unique constraint in the db
				userid, domain  = user.split('@')
				# set up for add alias user
				params = {'mode':1, # add alias users
						  'alias':cleaned_data['alias'],
						  'userid':userid,
						  'domain':domain
						 }
				# Add alias user
				aliasuseradded = model.managealiasuser(params)
				# Ensure no errors have occured
				if not aliasuseradded and model.error:
					# Make a new template context
					errors = {'form':form, 'new_data':new_data, 
							  'mode':mode, 'dberror':model.error }

					# User group responder to show errors
					return _groupmanageresponder(request, adict=errors)

		# If not valid form call responder with error
		else:
			errors = {'form':form,'new_data':new_data, 'mode':mode}
			return _groupmanageresponder(request, adict=errors)
			
	return HttpResponseRedirect (urlrel + 'admin/group/manage/')

@mustbe_admin
def groupedit(request, alias, domain):
	''' This method edits an existing alias of the system. it fills
		the form with the alias details and then awaits
		posted data from the user, validates said data, and
		if and error occurs uses the responder to display them 
		to the user. A succesfull post will update the alias using
		the viewdb function and redirect to avoid post problems '''

	# Create model instance
	model = AdminModel()
	# Set the mode
	mode ="edit"
	# Retrieve the requested alias.
 	request_alias =  model.getalias(alias, domain)
	# If there was no user in the db with this name or 
	# the function has thrown an error, we have been 
	# given bogus input data
	if ((request_alias and not request_alias.aliasname) or
	   (not request_alias and model.error)):
		# Raise alias has not be found
		raise Http404

	else:
		# Retrieve current alias users
		aliasusers = model.getaliasusers(alias, domain)
		# a list of users
		# associated to the domain of the alias 
		domain_users = DomainUsers(domain, 
								   model.getnondisabledusers(domain))
		request_users =[] 
		if aliasusers:
			request_users = [user.username for user in model.getaliasusers(alias, domain)]
		# Check we have posted data
		if request.method =="POST":
			# copy posted data
			new_data = request.POST.copy()
			# The selected users
			users = request.POST.getlist('users')
			# Update post dict
			new_data.update({'users':users})
			#  bind form instance
			form = GroupEdit(groupname=request_alias.aliasname, kargs=new_data)
			# Ensure for is valid
			if form.is_valid():
				# Clean the data
				cleaned_data = form.clean()
				# create function parameter list
				params = {'mode': 2,
						  'alias': request_alias.aliasname,
						  'domain': cleaned_data['domain'],
						  'new_alias': cleaned_data['alias'],
						  'notes': cleaned_data['notes']
						  }
				# call managealias in edit mode
				groupedited = model.managealias(params)
				# Ensure no errors have occured
				if not groupedited and model.error:
					errors = {'form':form, 'new_data':new_data,
							  'requestalias':request_alias, 'mode':mode,
							  'requestusers':request_users,
							  'domain_users':domain_users,
							  'dberror':model.error }
					return _groupmanageresponder(request, adict=errors)
				
				# Once the alias has been edit,
				# we update the selected users
				# Start by deleteing the previous alias users		
				if request_users:
					for user in request_users:
						# Split the string of usernames
						# These need to be usernames as that 
						# is the only unique constraint in the db
						userid, domain  = user.split('@')
						# All previously selected users
						params = {'mode':3, # add alias users
								  'alias':cleaned_data['alias'],
								  'userid':userid,
								  'domain':domain
								 }
						aliasuserdeleted = model.managealiasuser(params)
						if not aliasuserdeleted and model.error:
							errors = {'form':form, 'new_data':new_data, 
									  'mode':mode, 'dberror':model.error,
									  'domain_users':domain_users,
									  'requestusers':request_users}
							return _groupmanageresponder(request, adict=errors)

				# Add new users
				if users:
					for user in users:
						# Split the string of usernames
						# These need to be usernames as that 
						# is the only unique constraint in the db
						userid, domain  = user.split('@')
						# All previously selected users
						params = {'mode':1, # add alias users
								  'alias':cleaned_data['alias'],
								  'userid':userid,
								  'domain':domain
								 }
						aliasuseradded = model.managealiasuser(params)
						if not aliasuseradded and model.error:
							errors = {'form':form, 'new_data':new_data, 
									  'mode':mode, 'dberror':model.error,
									  'domain_users':domain_users,
									  'requestusers':request_users}
							return _groupmanageresponder(request, adict=errors)

				# Redirect to avoid post problems
				return HttpResponseRedirect (urlrel + 'admin/group/manage/')

			# If not valid call responder with error
			else:
				errors = {'form':form,'new_data':new_data, 
						  'mode':mode, 'requestalias':request_alias,
						  'domain_users':domain_users,
						  'requestusers':request_users}
				return _groupmanageresponder(request, adict=errors)
			
		return _groupmanageresponder(request, adict= {'requestalias':request_alias,
													  'requestusers':request_users,
													  'domain_users':domain_users,
													  'mode': mode})

	return HttpResponseRedirect(urlrel + 'admin/group/manage/')

@mustbe_admin
def groupdelete(request, alias, domain):
	''' This method deletes an existing group of the system. This
		will cause a cascading effect in the database, where by
		users of the group will be removed as well. '''

	# Create model instance
	model = AdminModel()
	# Set the mode
	mode ="add"
	# Retrieve the requested alias.
 	request_alias =  model.getalias(alias,domain)
	# Retrieve the requested alias users.
 	request_users =  model.getaliasusers(alias,domain)
	# If there was no alias in the db with this name or 
	# the function has thrown an error, we have been 
	# given bogus input data
	if (request_alias and not request_alias.aliasname) or (not
		request_alias and model.error):
		# Raise domain has not be found
		raise Http404

	else:
		params = {'mode': 3,
				  'alias': request_alias.aliasname,
				  'domain': request_alias.domainname,
				  'new_alias': None,
				  'notes':None 
				  }
	aliasdeleted = model.managealias(params)
	# Ensure no errors have occured
	if not aliasdeleted and model.error:
		errors = {'requestalias':request_alias, 'mode':mode,
				  'requestusers':request_users,
				  'dberror':model.error }
		
		return _groupmanageresponder(request, adict=errors)

	# Redirect to avoid post problems
	return HttpResponseRedirect (urlrel + 'admin/group/manage/')

######################### Helper methods ##################################

def _gen_pass(length=8, chars=string.letters + string.digits):

	# Create model instance
	model = AdminModel()
	# Assume the password exists
	exists = True	
	password = None
	while exists:
		# Create a 8 alphanumberic code
		password = ''.join([ choice(chars) for i in range(length) ])
		exists = model.checkpass(password)
		
	return password
		
	
class DomainUsers(object):

	def __init__(self, domainname, users =[]):
		self.domainname = domainname
		self.users = list(users)

	def __cmp__(self, other):
		if not isinstance (other, DomainUsers):
			return -1
		else:
			if self.domainname > other.domainname:
				return 1
			elif self.domainname == other.domainname:
				return 0 
			else:
				return -1

