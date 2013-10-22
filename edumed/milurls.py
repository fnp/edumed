from django.conf.urls import include, url, patterns

from fnpdjango.utils.urls import i18n_patterns
from .views import mil_home_view


urlpatterns = i18n_patterns('',
    url(r'^$', mil_home_view, name="mil_home"),
    url(r'^kompetencje/', include('curriculum.urls')),
    url(r'^wez-udzial/', include('comment.urls')),
    url(r'^zglos/', include('contact.urls')),
)

urlpatterns += patterns('',
    url(r'^kontakt/', 'django.contrib.flatpages.views.flatpage', {'url': 'kontakt/'},
        name="info_contact_pl"),
    url(r'^contact/', 'django.contrib.flatpages.views.flatpage', {'url': 'contact/'},
        name="info_contact_en"),
)

handler404 = 'edumed.views.mil_404_view'

from django.conf import settings
if settings.DEBUG:
    urlpatterns += patterns('',
        url(r'^media/(?P<path>.*)$', 'django.views.static.serve', {
            'document_root': settings.MEDIA_ROOT,
        }),
   )
