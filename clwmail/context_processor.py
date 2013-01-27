def urls_import(request):
	from clwmail import settings
	return {
		'urlmedia' : settings.MEDIA_URL,
		'urlfull' : settings.FULL_URL,
		'urlrel' : settings.RELATIVE_URL,
		'session_user':	   request.session['user']
	}
