# Django settings for Secret Santa project

DEBUG = True 
TEMPLATE_DEBUG = DEBUG

ADMINS = (
    ('', ''),
)
ADMIN_EMAIL = ''
MANAGERS = ADMINS
DEFAULT_FROM_EMAIL = ''

EMAIL_HOST = ''
EMAIL_HOST_USER = ''
EMAIL_HOST_PASSWORD = ''
# EMAIL_PORT = 
# EMAIL_USE_TLS = False

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'secretsanta',
        'HOST': '',
        'USER': '',
        'PASSWORD': ''
    }
}

TIME_ZONE = None
LANGUAGE_CODE = 'en-us'
SITE_ID = 1
USE_I18N = False
USE_L10N = True

MEDIA_ROOT = '/site_media/'
MEDIA_URL = '/site_media/'
ADMIN_MEDIA_PREFIX = '/media/'
STATIC_ROOT = ''
STATIC_URL = ''

STATICFILES_DIRS = (
)

STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
)

SECRET_KEY = ''

TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.load_template_source',
    'django.template.loaders.app_directories.load_template_source',
)

MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
)

ROOT_URLCONF = 'secretsanta.urls'

TEMPLATE_ROOT = ''
TEMPLATE_DIRS = (
    '/secretsanta/templates/'
)

INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.admin',
    'secretsanta.profiles',
    'secretsanta.registration',
)

ACCOUNT_ACTIVATION_DAYS = 1
AUTH_PROFILE_MODULE = 'profiles.ParticipantProfile'

LOGOUT_URL = '/login/'

try:
    from local_settings import *
except ImportError:
    import sys
    sys.stderr.write( "local_settings.py not set; using default settings" )

