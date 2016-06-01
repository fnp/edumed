# -*- coding: utf-8 -*-
from django.contrib.flatpages.views import flatpage
from django.core.exceptions import ValidationError
from django.core.validators import EmailValidator
from django.http.response import HttpResponseRedirect
from django.shortcuts import render_to_response
from django.template.context import RequestContext
from django.views.defaults import page_not_found
from django.views.generic import TemplateView
from pybb.views import ProfileEditView

from contact.models import Contact
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


class AvatarlessProfileEditView(ProfileEditView):
    form_class = AvatarlessEditProfileForm


def olimpiada_teaser(request):
    if request.POST:
        email = request.POST.get('email')
        try:
            EmailValidator()(email)
            Contact.objects.create(
                contact=email,
                body={},
                ip=request.META['REMOTE_ADDR'],
                form_tag='olimpiada-teaser')
        except ValidationError:
            pass
        return HttpResponseRedirect(request.path)
    return render_to_response('olimpiada_teaser.html', context_instance=RequestContext(request))
