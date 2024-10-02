# -*- coding: utf-8 -*-
import os


ADMINS = [
    tuple(adm.split(':'))
    for adm in
    os.environ.get('ADMINS', '').split('\n')
    if adm
]

MANAGERS = [
    tuple(adm.split(':'))
    for adm in
    os.environ.get('MANAGERS', os.environ.get('ADMINS', '')).split('\n')
    if adm
]

DEBUG = False

if 'DB_NAME' in os.environ:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql_psycopg2',
            'NAME': os.environ['DB_NAME'],
            'USER': os.environ.get('DB_USER', ''),
            'PASSWORD': os.environ.get('DB_PASSWORD', ''),
            'HOST': os.environ.get('DB_HOST', ''),
            'PORT': os.environ.get('DB_PORT', ''),
        }
    }
else:
    DEBUG = True

    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': '/app/var/dev.db',
        }
    }


DEBUG = os.environ.get('DEBUG', str(DEBUG)).lower() == 'true'

ALLOWED_HOSTS = os.environ.get('ALLOWED_HOSTS', '').split()

SERVER_EMAIL = os.environ.get('SERVER_EMAIL', 'no-reply@edukacjamedialna.edu.pl')
EMAIL_HOST = os.environ.get('EMAIL_HOST', 'localhost')
DEFAULT_FROM_EMAIL = os.environ.get('DEFAULT_FROM_EMAIL', 'no-reply@edukacjamedialna.edu.pl')
EMAIL_SUBJECT_PREFIX = os.environ.get('EMAIL_SUBJECT_PREFIX', '[EdukacjaMedialna.edu.pl] ')

PIWIK_URL = os.environ.get('PIWIK_URL', '')
PIWIK_SITE_ID = int(os.environ.get('PIWIK_SITE_ID', '0'))
SECRET_KEY = os.environ.get('SECRET_KEY', '')

MAILCHIMP_API_KEY = os.environ.get('MAILCHIMP_API_KEY', '')
MAILCHIMP_LIST_ID = os.environ.get('MAILCHIMP_LIST_ID', '')
MAILCHIMP_GROUP_ID = os.environ.get('MAILCHIMP_GROUP_ID', '')


FNPDJANGO_REALIP = True
FNPDJANGO_XACCEL = False

TEMPLATE_DEBUG = DEBUG

SITE_ID = 1

# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
    # 'django.template.loaders.eggs.Loader',
)

ROOT_URLCONF = 'edumed.urls'

SUBDOMAIN_URLCONFS = {
    None: 'edumed.urls',
    'katalog': 'edumed.milurls',
}

# Python dotted path to the WSGI application used by Django's runserver.
WSGI_APPLICATION = 'edumed.wsgi.application'

TEMPLATE_DIRS = (
    # Put strings here, like "/home/html/django_templates" or "C:/www/django/templates".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
)

if DEBUG:
    EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
    ALLOWED_HOSTS = ALLOWED_HOSTS or ['*']
    SECRET_KEY = SECRET_KEY or 'dev-secret-key'
