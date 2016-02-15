from django.conf.urls import patterns, include, url
from django.conf import settings
from .views import HomeView, AvatarlessProfileEditView



urlpatterns = patterns('',
    url(r'^$', HomeView.as_view(), name="home"),
    url(r'^lekcje/', include('catalogue.urls')),
    url(r'^info/(?P<url>.*)$', 'django.contrib.flatpages.views.flatpage',
        name="info"),
    url(r'^szukaj/', include('haystack.urls')),
    url(r'^zglos/', include('contact.urls')),
    url(r'^forum/profile/edit/$', AvatarlessProfileEditView.as_view(), name='edit_profile'),
    url(r'^forum/', include('forum.urls')),
    url(r'^forum/', include('pybb.urls', namespace='pybb')),
    url(r'^kompetencje/', include('curriculum.urls')),
    #url(r'^wtem/', include('wtem.urls')),
    url(r'^tem/', include('wtem.urls')),
)


# Admin stuff, if necessary.
if 'django.contrib.admin' in settings.INSTALLED_APPS:
    from django.contrib import admin
    admin.autodiscover()

    if 'django_cas' in settings.INSTALLED_APPS:
        urlpatterns += patterns('',
            (r'^admin/logout/$', 'django_cas.views.logout'),
        )
    urlpatterns += patterns('',
        url(r'^admin/doc/', include('django.contrib.admindocs.urls')),
        url(r'^admin/', include(admin.site.urls)),
    )

# Auth stuff, if necessary
if 'django_cas' in settings.INSTALLED_APPS:
    urlpatterns += patterns('',
        url(r'^accounts/login/$', 'django_cas.views.login', name='login'),
        url(r'^accounts/logout/$', 'django_cas.views.logout', name='logout'),
    )


if settings.DEBUG:
    from fnpdjango.utils.urls import i18n_patterns
    from .views import mil_home_view, mil_contact_view, mil_knowledge_base_view
    urlpatterns += i18n_patterns(
        '',
        url(r'^katalog/$', mil_home_view, name="mil_home"),
        url(r'^wez-udzial/', include('comment.urls')),
        url(r'^kontakt/$', mil_contact_view, name='mil_contact'),
        url(r'^bazawiedzy/(?P<url>.*)$', mil_knowledge_base_view, name="knowledge_base"),
    )


if settings.DEBUG:
    urlpatterns += patterns('',
        url(r'^media/(?P<path>.*)$', 'django.views.static.serve', {
            'document_root': settings.MEDIA_ROOT,
        }),
   )
