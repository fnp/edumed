# -*- coding: utf-8 -*-
from edumed.utils import process_app_deps

TEMPLATE_CONTEXT_PROCESSORS = process_app_deps((
    ("django.contrib.auth.context_processors.auth", "django.contrib.auth"),
    "django.core.context_processors.debug",
    "django.core.context_processors.i18n",
    "django.core.context_processors.media",
    "django.core.context_processors.static",
    "django.core.context_processors.tz",
    ("django.contrib.messages.context_processors.messages", 'django.contrib.messages'),
    "django.core.context_processors.request",
    'pybb.context_processors.processor',
    'edumed.context_processors.base_template',
))
