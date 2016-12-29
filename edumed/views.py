# -*- coding: utf-8 -*-
from django.contrib.flatpages.views import flatpage
from django.views.defaults import page_not_found
from django.views.generic import TemplateView

from .forms import AvatarlessEditProfileForm


class HomeView(TemplateView):
    template_name = "home.html"


def mil_home_view(request):
    return flatpage(request, url='/' if request.LANGUAGE_CODE == 'pl' else '/en/')


def mil_404_view(request):
    return page_not_found(request, '404_mil.html')


def mil_contact_view(request):
    return flatpage(request, url='/kontakt_mil/' if request.LANGUAGE_CODE == 'pl' else '/contact_mil/')


def mil_knowledge_base_view(request, url):
    return flatpage(request, url='bazawiedzy/' + url)


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
    from django.conf import settings
    from django.contrib.flatpages.models import FlatPage
    from django.contrib.flatpages.views import render_flatpage
    from django.contrib.sites.models import get_current_site
    from django.http.response import Http404, HttpResponsePermanentRedirect
    from django.shortcuts import get_object_or_404
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
