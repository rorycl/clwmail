from django.conf.urls.defaults import *
urlpatterns = patterns('clwmail.mail_auth.views',
    (r'index/$'        , 'login'),
	(r'login/$'		   , 'login'),
    (r'logout/$'        , 'logout'),
	(r'deny/(?P<item>.*)/$',			 'deny'),
)
