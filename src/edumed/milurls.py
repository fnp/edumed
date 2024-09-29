# -*- coding: utf-8 -*-
from django.conf.urls import include, url, patterns
from django.conf import settings

from fnpdjango.utils.urls import i18n_patterns
from .views import mil_home_view, mil_contact_view, mil_knowledge_base_view


urlpatterns = i18n_patterns(
    '',
    url(r'^$', mil_home_view, name="mil_home"),
    url(r'^kompetencje/', include('curriculum.urls')),
    url(r'^wez-udzial/', include('comment.urls')),
    url(r'^zglos/', include('contact.urls')),
    url(r'^kontakt/$', mil_contact_view, name='mil_contact'),
    url(r'^bazawiedzy/(?P<url>.*)$', mil_knowledge_base_view,
        name="knowledge_base"),
)

handler404 = 'edumed.views.mil_404_view'

if settings.DEBUG:
    urlpatterns += patterns(
        '',
        url(r'^media/(?P<path>.*)$', 'django.views.static.serve', {
            'document_root': settings.MEDIA_ROOT,
        }),
    )
