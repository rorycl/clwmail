from django.conf.urls.defaults import *
from clwmail import settings 
rrel = settings.RELATIVE_URL[1:]

urlpatterns = patterns('clwmail.mailstore.views',
    (r'user/(?P<username>.*)/domain/(?P<domain>.*)/holiday/(?P<hol_id>\d{1,})/delete/$'        , 'holidaydelete'),
    (r'user/(?P<username>.*)/domain/(?P<domain>.*)/leave/off/$'        , 'leaveoff'),
    (r'user/(?P<username>.*)/domain/(?P<domain>.*)/holiday/(?P<hol_id>\d{1,})/edit/$'        , 'holidayedit'),
    (r'user/(?P<username>.*)/domain/(?P<domain>.*)/holiday/add/$'        , 'holidayadd'),
    (r'user/(?P<username>.*)/domain/(?P<domain>.*)/holiday/$'        , 'holiday'),
    (r''        , 'holiday'),
)
