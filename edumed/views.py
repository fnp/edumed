# -*- coding: utf-8 -*-
from django.contrib.flatpages.views import flatpage
from django.views.defaults import page_not_found
from django.views.generic import TemplateView
from pybb.views import ProfileEditView

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
