from django.contrib.auth.models import AnonymousUser
class AuthSession:

	def process_request(self,request):
		user = None
		if hasattr(request,'session'):
			try:
				user =request.session['user']
			except KeyError:
				request.session['user'] = AnonymousUser()
			else:
				pass
