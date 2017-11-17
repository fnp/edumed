# -*- coding: utf-8 -*-
from django.conf.urls import include, url
from django.conf import settings
from django.contrib.flatpages.views import flatpage

urlpatterns = [
    url(r'^szukaj/', include('haystack.urls')),

    url(r'^zglos/', include('contact.urls')),
    url(r'^zadania/', include('wtem.urls')),
    url(r'^drugi-etap/', include('stage2.urls')),
]


# Admin stuff, if necessary.
if 'django.contrib.admin' in settings.INSTALLED_APPS:
    from django.contrib import admin
    admin.autodiscover()

    if 'django_cas' in settings.INSTALLED_APPS:
        urlpatterns += [
            url(r'^admin/logout/$', 'django_cas.views.logout'),
        ]
    urlpatterns += [
        url(r'^admin/doc/', include('django.contrib.admindocs.urls')),
        url(r'^admin/', include(admin.site.urls)),
    ]

# Auth stuff, if necessary
if 'django_cas' in settings.INSTALLED_APPS:
    urlpatterns += [
        url(r'^accounts/login/$', 'django_cas.views.login', name='login'),
        url(r'^accounts/logout/$', 'django_cas.views.logout', name='logout'),
    ]
else:
    from django.contrib.auth.views import login, logout
    urlpatterns += [
        url(r'^accounts/login/$', login, name='login'),
        url(r'^accounts/logout/$', logout, name='logout'),
    ]

urlpatterns += (
    url(r'^(?P<url>[^/]*/|)$',
        lambda request, url: flatpage(request, 'turniej/' + url)),
)
