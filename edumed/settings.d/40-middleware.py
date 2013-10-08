MIDDLEWARE_CLASSES = tuple(x for x in (
    'django.middleware.cache.UpdateCacheMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware'
            if "django.contrib.sessions" in INSTALLED_APPS else None,
    #'django.middleware.locale.LocaleMiddleware',
    'fnpdjango.middleware.URLLocaleMiddleware',

    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'honeypot.middleware.HoneypotMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware'
            if "django.contrib.auth" in INSTALLED_APPS else None,
    'django_cas.middleware.CASMiddleware'
            if "django_cas" in INSTALLED_APPS else None,
    'django.contrib.messages.middleware.MessageMiddleware'
            if "django.contrib.messages" in INSTALLED_APPS else None,
    'piwik.django.middleware.PiwikMiddleware'
            if "piwik.django" in INSTALLED_APPS else None,
    # Uncomment the next line for simple clickjacking protection:
    # 'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'pagination.middleware.PaginationMiddleware'
            if "pagination" in INSTALLED_APPS else None,
    'django.middleware.cache.FetchFromCacheMiddleware',
    'fnpdjango.middleware.SetRemoteAddrFromXRealIP',
    'pybb.middleware.PybbMiddleware',
    'forum.middleware.ForumMiddleware'
) if x is not None)
