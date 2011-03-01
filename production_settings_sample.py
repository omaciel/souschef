# Production settings for souschef project.

DEBUG = False
TEMPLATE_DEBUG = DEBUG

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3', # Add 'postgresql_psycopg2', 'postgresql', 'mysql', 'sqlite3' or 'oracle'.
        'NAME': 'production.db',                      # Or path to database file if using sqlite3.
        'USER': '',                      # Not used with sqlite3.
        'PASSWORD': '',                  # Not used with sqlite3.
        'HOST': '',                      # Set to empty string for localhost. Not used with sqlite3.
        'PORT': '',                      # Set to empty string for default. Not used with sqlite3.
    }
}

SITE_HOST = '127.0.0.1:8000'
DEFAULT_FROM_EMAIL = \
    'Conary Recipes <contact@conaryrecipes.com>'
EMAIL_HOST = 'mail.example.com'
EMAIL_PORT = ''
EMAIL_HOST_USER = 'contact@example.com'
EMAIL_HOST_PASSWORD = ''
