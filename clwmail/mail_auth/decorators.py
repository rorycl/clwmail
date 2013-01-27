from django.contrib.auth import authenticate
from django.contrib.auth.models import AnonymousUser 
from django.template import RequestContext 
from django.http import HttpResponseRedirect
from django.http import HttpResponse
from django.shortcuts import render_to_response 
from clwmail import settings

urlrel = settings.RELATIVE_URL

# This method ensures that the user
# trying to see a specific view 
# has been authenticated and 

def must_login (view_function):
	def check_user(request,*args,**kargs):
		try:
			user =request.session['user']
		except KeyError:
			request.session['user'] = AnonymousUser()
			return HttpResponseRedirect(urlrel + 'auth/login/')

		else:
			if user.is_authenticated(): 
				return 	view_function(request,*args,**kargs)
			else:
				# if the user was not logged in and requested a page
				# then store the requested url to redirect to post login.
				request.session['pre_auth_url'] = request.path

			return HttpResponseRedirect(urlrel + 'auth/login/')
	return check_user


# This method ensures that the user
# trying to see a specific view 
# has been authenticated and IS an
# admin
def mustbe_admin (view_function):
	def check_user(request,*args,**kargs):
		try:
			user =request.session['user']
		except KeyError:
			request.session['user'] = AnonymousUser()
			return HttpResponseRedirect(urlrel + 'auth/login/')

		else:
			if user.is_authenticated():
				if user.b_isadmin:
					return 	view_function(request,*args,**kargs)
				else:
					return HttpResponseRedirect(urlrel + 'mailstore/user/%s/domain/%s/holiday/' % 
																	(user.username, user.domain))
			else:
				# if the user was not logged in and requested a page
				# then store the requested url to redirect to post login.
				request.session['pre_auth_url'] = request.path

			return HttpResponseRedirect(urlrel + 'auth/login/')
	return check_user

