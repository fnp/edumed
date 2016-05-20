# -*- coding: utf-8 -*-
from edumed.utils import process_app_deps

MIDDLEWARE_CLASSES = process_app_deps((
    'django.middleware.cache.UpdateCacheMiddleware',
    ('django.contrib.sessions.middleware.SessionMiddleware', 'django.contrib.sessions'),
    # 'django.middleware.locale.LocaleMiddleware',
    'subdomains.middleware.SubdomainURLRoutingMiddleware',
    'fnpdjango.middleware.URLLocaleMiddleware',

    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'honeypot.middleware.HoneypotMiddleware',
    ('django.contrib.auth.middleware.AuthenticationMiddleware', 'django.contrib.auth'),
    ('django_cas.middleware.CASMiddleware', 'django_cas'),
    ('django.contrib.messages.middleware.MessageMiddleware', 'django.contrib.messages'),
    # Uncomment the next line for simple clickjacking protection:
    # 'django.middleware.clickjacking.XFrameOptionsMiddleware',
    ('pagination.middleware.PaginationMiddleware', 'pagination'),
    'django.middleware.cache.FetchFromCacheMiddleware',
    'fnpdjango.middleware.SetRemoteAddrFromXRealIP',
    'pybb.middleware.PybbMiddleware',
    'forum.middleware.ForumMiddleware',
    'wtem.middleware.ThreadLocalMiddleware'
))
