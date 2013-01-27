from clwmail.mail_auth.sql.viewdb import AuthModel 
from django.http import Http404

def canview (request, userid, domain):
	'''This method ensures that current user is eligable to see the requested
	page. It first checks to see that the passed in userid and domain is a
	valid entry in the database. If so, the session user (accessed via the
	request object) is examined. Being an administrator of the system ensures
	that all valid requests are viewable. A standard user must match the 
	the crendentials stored in the session against the requested page. If no
	conditions are met it returns false by default. This method should only
	be called in a view method as it requires the instance of the HttpRequest
	object.'''

	# Create model instance
	model = AuthModel()
	# The requested page owner
	request_user = model.getuser(userid, domain)
	# If there is no such user or the function
	# threw and error raise a page not found
	# exception
	if ((request_user and not request_user.userid) or 
	   (not request_user and model.error)):
		raise Http404
	# Now that we have ensured the requested page 
	# actually belongs to someone, see if the current
	# session viewer is allowed to see it.
	try:
		session_user = request.session['user']
	except KeyError:
		# If there is no user then
		# we return False
		return False 
	else:
		#  if the user admin it will always be viewable
		if session_user.b_isadmin:
			return True

		# If the user is not an admin then check that the requested page
		# belongs to the session user. This will only be the case
		# if the domain and userid of the requested page match that
		# of the logged in user.
		elif (session_user.username == userid and 
				session_user.domain == domain):
			return True

		else:
			return False

	return False
			
		
		



			

