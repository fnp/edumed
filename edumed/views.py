import os.path
from django.conf import settings
from django.views.generic import TemplateView
from django.views.defaults import page_not_found
from pybb.views import ProfileEditView
from .forms import AvatarlessEditProfileForm


class HomeView(TemplateView):
    template_name="home.html"

    def get_context_data(self, **kwargs):
        context = super(HomeView, self).get_context_data(**kwargs)
        context['package_url'] = os.path.join(settings.MEDIA_URL, settings.CATALOGUE_PACKAGE)
        context['package_student_url'] = os.path.join(settings.MEDIA_URL, settings.CATALOGUE_PACKAGE_STUDENT)
        return context


class MILHomeView(TemplateView):
    template_name = 'home_mil.html'

def mil_404_view(request):
    return page_not_found(request, '404_mil.html')

class AvatarlessProfileEditView(ProfileEditView):
    form_class = AvatarlessEditProfileForm
