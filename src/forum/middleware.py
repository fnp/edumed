# -*- coding: utf-8 -*-
from urllib import urlencode

from django.contrib.auth import REDIRECT_FIELD_NAME
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django_cas.views import login as cas_login


class ForumMiddleware(object):
    @staticmethod
    def process_request(request):
        if request.path.startswith(reverse('pybb:index')) \
                and (not hasattr(request, 'user') or not request.user.is_authenticated()):
            params = urlencode({REDIRECT_FIELD_NAME: request.get_full_path()})
            return HttpResponseRedirect(reverse(cas_login) + '?' + params)
