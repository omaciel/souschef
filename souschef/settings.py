# Django settings for souschef project.

import os.path
from django.conf.global_settings import TEMPLATE_CONTEXT_PROCESSORS

PROJECT_PATH = os.path.dirname(os.path.abspath(__file__))

DEBUG = True
TEMPLATE_DEBUG = DEBUG

ADMINS = (
    # ('Your Name', 'your_email@domain.com'),
)

MANAGERS = ADMINS

DATABASE_ENGINE = 'sqlite3'           # 'postgresql_psycopg2', 'postgresql', 'mysql', 'sqlite3' or 'oracle'.
DATABASE_NAME = 'foo.db'             # Or path to database file if using sqlite3.
DATABASE_USER = ''             # Not used with sqlite3.
DATABASE_PASSWORD = ''         # Not used with sqlite3.
DATABASE_HOST = ''             # Set to empty string for localhost. Not used with sqlite3.
DATABASE_PORT = ''             # Set to empty string for default. Not used with sqlite3.

# Local time zone for this installation. Choices can be found here:
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
# although not all choices may be available on all operating systems.
# If running in a Windows environment this must be set to the same as your
# system time zone.
TIME_ZONE = 'America/New_York'

# Language code for this installation. All choices can be found here:
# http://www.i18nguy.com/unicode/language-identifiers.html
LANGUAGE_CODE = 'en-us'

SITE_ID = 1

# If you set this to False, Django will make some optimizations so as not
# to load the internationalization machinery.
USE_I18N = True

# Absolute path to the directory that holds media.
# Example: "/home/media/media.lawrence.com/"
MEDIA_ROOT = os.path.join(PROJECT_PATH, "media")

# URL that handles the media served from MEDIA_ROOT. Make sure to use a
# trailing slash if there is a path component (optional in other cases).
# Examples: "http://media.lawrence.com", "http://example.com/media/"
MEDIA_URL = '/site_media/'

# URL prefix for admin media -- CSS, JavaScript and images. Make sure to use a
# trailing slash.
# Examples: "http://foo.com/media/", "/media/".
ADMIN_MEDIA_PREFIX = '/media/'

# Make this unique, and don't share it with anybody.
SECRET_KEY = 't6&w@k)srt%aj6g$j^s@=*s-04=8#7ga7lqbbih#&*lt(7ufj='

# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.load_template_source',
    'django.template.loaders.app_directories.load_template_source',
#     'django.template.loaders.eggs.load_template_source',
)

MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
)

ROOT_URLCONF = 'souschef.urls'

TEMPLATE_DIRS = (
    # Put strings here, like "/home/html/django_templates" or "C:/www/django/templates".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
    os.path.join(PROJECT_PATH, 'templates'),
)

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    # Django modules used
    'favorites',
    'tagging',
    'userprofile',
    # Application modules
    'aboyeur',
    'demoprofile',
)

# START of django-profile specific options
AUTH_PROFILE_MODULE = 'demoprofile.profile'

I18N_URLS = False
DEFAULT_AVATAR = os.path.join(MEDIA_ROOT, 'userprofile/generic.jpg')
AVATAR_WEBSEARCH = False
# 127.0.0.1:8000 Google Maps API Key
GOOGLE_MAPS_API_KEY = "ABQIAAAAn7xaxKrYcZCx8cCWR6ZTfBT2yXp_ZAY8_ufC3CFXhHIE1NvwkxTgN-5NZeq0BNNl0GOETNs2UCGSEw"
# Haddock
#GOOGLE_MAPS_API_KEY="ABQIAAAA06IJoYHDPFMx4u3hTtaghxS1mGAeXhF8eEwoOC3WUqD9xSVHbhT_wvgbriWemZzoPwFT5-HqnLJ9-A"
REQUIRE_EMAIL_CONFIRMATION = False
AVATAR_QUOTA = 8
