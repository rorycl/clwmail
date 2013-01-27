from django.conf.urls.defaults import *
from clwmail import settings 

rrel = settings.RELATIVE_URL[1:]
media_url = settings.MEDIA_URL[1:]

urlpatterns = patterns('',
    (r'^'+ rrel + 'mailstore/' ,include('clwmail.mailstore.urls')),
    (r'^'+ rrel + 'auth/' 	   ,include('clwmail.mail_auth.urls')),
    (r'^'+ rrel + 'admin/' 	   ,include('clwmail.admin.urls')),
    (r'^' + media_url + '(.*)$' 	,'django.views.static.serve',
														  {'document_root':
														  settings.MEDIA_ROOT,
														  'show_indexes':True})         ,

	(r''		 ,'clwmail.mail_auth.views.login'),


)
