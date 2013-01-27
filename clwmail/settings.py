# Django settings for clwmail.
#
# required packages - python-psycopg2, python-psycopg, python-2.5, python-django (1.0)
#					  clwsoftware repos
#
# Below settings file to be edited for each installation IMPORTANT: note "mailstore home"
# and UID/GID settings near the bottom of this file.
#
# Configuration also needs to take place in apache.
#
# After all settings changed and testing completed - set DEBUG to False

INSTALL_ROOT ='/var/www/clwmail/';

DEBUG = True
TEMPLATE_DEBUG = DEBUG

ADMINS = (
    ('rory', 'rory@campbell-lange.net'),
)

MANAGERS = ADMINS

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'clwmail',
        'USER': 'user',
        'PASSWORD': 'password',
        'HOST': '', # leave empty for localhost domain socket
        'PORT': '',
    }
}

# Local time zone for this installation. Choices can be found here:
# http://www.postgresql.org/docs/8.1/static/datetime-keywords.html#DATETIME-TIMEZONE-SET-TABLE
# although not all variations may be possible on all operating systems.
# If running in a Windows environment this must be set to the same as your
# system time zone.
TIME_ZONE = 'Europe/London'

# Language code for this installation. All choices can be found here:
# http://www.w3.org/TR/REC-html40/struct/dirlang.html#langcodes
# http://blogs.law.harvard.edu/tech/stories/storyReader$15
LANGUAGE_CODE = 'en-us'

SITE_ID = 1

# If you set this to False, Django will make some optimizations so as not
# to load the internationalization machinery.
USE_I18N = True

# Absolute path to the directory that holds media.
# Example: "/home/media/media.lawrence.com/"

# Absolute path to the directory that holds media.
# Example: "/home/media/media.lawrence.com/"
MEDIA_ROOT =INSTALL_ROOT + 'clwmail/media/'

# URL that handles the media served from MEDIA_ROOT.
# Example: "http://media.lawrence.com"

FULL_URL = 'http://localhost/clwmail/'
RELATIVE_URL = '/clwmail/'
MEDIA_URL = '/clwmail/media/'

# URL prefix for admin media -- CSS, JavaScript and images. Make sure to use a
# trailing slash.
# Examples: "http://foo.com/media/", "/media/".
ADMIN_MEDIA_PREFIX = '/media/'

# Make this unique, and don't share it with anybody.
SECRET_KEY = '*9$r40mxxxxchangeme!!!*(())())tcni7kblgf$a)grc=%te'

# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
	'clwmail.mail_auth.middleware.AuthSession',
)

ROOT_URLCONF = 'clwmail.urls'

TEMPLATE_DIRS = (
    # Put strings here, like "/home/html/django_templates" or "C:/www/django/templates".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
	INSTALL_ROOT + 'templates/',
)

TEMPLATE_CONTEXT_PROCESSORS = (
    'django.core.context_processors.debug',
    #'django.core.context_processors.i18n',
    'django.core.context_processors.media',
    'django.core.context_processors.static',
    'django.core.context_processors.static',
    #'django.contrib.messages.context_processors.messages',
    'clwauth.context_processor.urls',
    'clwauth.context_processor.navigation',
)

INSTALLED_APPS = (
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'clwmail.mailstore',
    'clwmail.mail_auth',
    'clwmail.utils',
    'clwmail.admin',
    'clwmail.exim',
)

SESSION_COOKIE_NAME = 'CLWMail_v2'

SESSION_EXPIRE_AT_BROWSER_CLOSE = True

# http://www.b-list.org/weblog/2006/06/14/django-tips-template-context-processors
TEMPLATE_CONTEXT_PROCESSORS = (#"django.core.context_processors.auth",
                               "django.core.context_processors.debug",
                               "django.core.context_processors.i18n",
                               "clwmail.context_processor.urls_import",)


STATUS_MAPPER ={1:'Active', 2:'Holiday', 9:'Inactive'}

# If the userid is not wanted. You must change
# the useradd view function in admin/views.py
# %s = placeholder for userid (taken automatically from DB)

MAILSTORE_HOME = '/mailusersdirector/%s/Maildir'
UID =1001
GID =1001

ITEMS_PER_PAGE = 30

TYPERS = ['person','project']

CALENDAR_URL = MEDIA_URL +'javascript/calendar2/'
