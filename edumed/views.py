# -*- coding: utf-8 -*-
from django.conf import settings
from django.contrib.flatpages.models import FlatPage
from django.contrib.flatpages.views import render_flatpage
from django.contrib.sites.models import get_current_site
from django.http.response import Http404, HttpResponsePermanentRedirect
from django.shortcuts import get_object_or_404
from django.views.generic import TemplateView


def flatpage_with_template(request, url, template_name):
    """
    Public interface to the flat page view.

    Models: `flatpages.flatpages`
    Templates: Uses the template defined by the ``template_name`` field,
        or :template:`flatpages/default.html` if template_name is not defined.
    Context:
        flatpage
            `flatpages.flatpages` object
    """
    if not url.startswith('/'):
        url = '/' + url
    site_id = get_current_site(request).id
    try:
        f = get_object_or_404(FlatPage, url__exact=url, sites__id__exact=site_id)
    except Http404:
        if not url.endswith('/') and settings.APPEND_SLASH:
            url += '/'
            get_object_or_404(FlatPage, url__exact=url, sites__id__exact=site_id)
            return HttpResponsePermanentRedirect('%s/' % request.path)
        else:
            raise
    f.template_name = template_name
    return render_flatpage(request, f)
