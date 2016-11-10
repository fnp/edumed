# -*- coding: utf-8 -*-
from django.conf.urls import patterns, include, url
from django.conf import settings
from django.contrib.flatpages.views import flatpage
from django.shortcuts import redirect

from .views import HomeView, AvatarlessProfileEditView, flatpage_with_template

urlpatterns = patterns(
    '',
    # url(r'^$', HomeView.as_view(), name="home"),
    # url(r'^lekcje/', include('catalogue.urls')),
    # url(r'^info/turniej/(?P<url>.*)$', lambda request, url: redirect('olimpiada', url)),
    # url(r'^info/(?P<url>.*)$', flatpage, name="info"),
    # url(r'^olimpiada/$', lambda request: flatpage(request, 'turniej/'), name='olimpiada'),
    # url(r'^olimpiada/(?P<url>.*)$', lambda request, url: flatpage(request, 'turniej/' + url), name='olimpiada'),
    # url(r'^szukaj/', include('haystack.urls')),

    # url(r'^olimpiada-teaser/(?P<url>.*)$',
    #     lambda request, url: flatpage_with_template(request, 'turniej/' + url, 'olimpiada_teaser.html'),
    #     name='olimpiada_teaser'),

    url(r'^zglos/', include('contact.urls')),
    # url(r'^forum/profile/edit/$', AvatarlessProfileEditView.as_view(), name='edit_profile'),
    # url(r'^forum/', include('forum.urls')),
    # url(r'^forum/', include('pybb.urls', namespace='pybb')),
    # url(r'^kompetencje/', include('curriculum.urls')),
    url(r'^zadania/', include('wtem.urls')),
)


# Admin stuff, if necessary.
if 'django.contrib.admin' in settings.INSTALLED_APPS:
    from django.contrib import admin
    admin.autodiscover()

    if 'django_cas' in settings.INSTALLED_APPS:
        urlpatterns += patterns(
            '',
            (r'^admin/logout/$', 'django_cas.views.logout'),
        )
    urlpatterns += patterns(
        '',
        url(r'^admin/doc/', include('django.contrib.admindocs.urls')),
        url(r'^admin/', include(admin.site.urls)),
    )

# Auth stuff, if necessary
if 'django_cas' in settings.INSTALLED_APPS:
    urlpatterns += patterns(
        '',
        url(r'^accounts/login/$', 'django_cas.views.login', name='login'),
        url(r'^accounts/logout/$', 'django_cas.views.logout', name='logout'),
    )

urlpatterns += (
    url(r'^(?P<url>[^/]*/|)$',
        lambda request, url: flatpage_with_template(request, 'turniej/' + url, 'olimpiada_teaser.html')),
)

if settings.DEBUG:
    urlpatterns += patterns(
        '',
        url(r'^media/(?P<path>.*)$', 'django.views.static.serve', {
            'document_root': settings.MEDIA_ROOT,
        }),
    )
