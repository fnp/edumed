from django.conf.urls import patterns, include, url
from django.conf import settings
from django.views.generic import TemplateView


urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'edumed.views.home', name='home'),
    url(r'^$', TemplateView.as_view(template_name="home.html"), name="home"),
    url(r'^kompetencje/', include('curriculum.urls')),
    url(r'^lekcje/', include('catalogue.urls')),
#    url(r'^i/', include('django.contrib.flatpages.urls')),
    url(r'^i/(?P<url>.*)$', 'django.contrib.flatpages.views.flatpage',
        name="info"),
    url(r'^szukaj/', include('haystack.urls')),
)


# Admin stuff, if necessary.
if 'django.contrib.admin' in settings.INSTALLED_APPS:
    from django.contrib import admin
    admin.autodiscover()

    urlpatterns += patterns('',
        url(r'^admin/doc/', include('django.contrib.admindocs.urls')),
        url(r'^admin/', include(admin.site.urls)),
    )

# Auth stuff, if necessary
if 'django_cas' in settings.INSTALLED_APPS:
    urlpatterns += patterns('',
        (r'^accounts/login/$', 'django_cas.views.login'),
        (r'^accounts/logout/$', 'django_cas.views.logout'),
    )


if settings.DEBUG:
    urlpatterns += patterns('',
        url(r'^media/(?P<path>.*)$', 'django.views.static.serve', {
            'document_root': settings.MEDIA_ROOT,
        }),
   )
