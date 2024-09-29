# -*- coding: utf-8 -*-
from .apps import INSTALLED_APPS

if 'django_cas' in INSTALLED_APPS:
    AUTHENTICATION_BACKENDS = (
        'django.contrib.auth.backends.ModelBackend',
        'fnpdjango.auth_backends.AttrCASBackend',
    )
