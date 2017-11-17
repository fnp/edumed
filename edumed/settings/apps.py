# -*- coding: utf-8 -*-

INSTALLED_APPS = (
    'edumed',
    'wtem',
    'stage2',

    'fnpdjango',
    'south',
    'pipeline',
    'django_extensions',
    # Disable, if not using Piwik.
    'piwik',
    # Disable, if not using CAS.
    'honeypot',
    'django_cas',
    'sponsors',
    'haystack',
    'chunks',
    'contact',
    'django_libravatar',
    'sorl.thumbnail',
    'subdomains',

    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.admin',
    'django.contrib.admindocs',
    'django.contrib.flatpages',
    'django.contrib.humanize'
)
