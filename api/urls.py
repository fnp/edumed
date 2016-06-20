# -*- coding: utf-8 -*-
from django.conf.urls import patterns, url
from django.views.decorators.csrf import csrf_exempt
from piston.authentication import OAuthAuthentication, oauth_access_token
from piston.resource import Resource

from api import handlers
from api.helpers import CsrfExemptResource

auth = OAuthAuthentication(realm="Edukacja Medialna")

lesson_list_resource = CsrfExemptResource(handler=handlers.LessonsHandler, authentication=auth)
lesson_resource = Resource(handler=handlers.LessonDetailHandler)

urlpatterns = patterns(
    'piston.authentication',
    url(r'^oauth/request_token/$', 'oauth_request_token'),
    url(r'^oauth/authorize/$', 'oauth_user_auth'),
    url(r'^oauth/access_token/$', csrf_exempt(oauth_access_token)),
)

urlpatterns += patterns(
    '',
    # url(r'^$', TemplateView.as_view(template_name='api/main.html'), name='api'),

    # objects details
    url(r'^lessons/(?P<lesson>[a-z0-9-]+)/$', lesson_resource, name="api_lesson"),

    # lessons
    url(r'^lessons/$', lesson_list_resource, name='api_lesson_list'),
)
