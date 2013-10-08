import os.path
from django.conf import settings
from django.views.generic import TemplateView
from pybb.views import ProfileEditView
from .forms import AvatarlessEditProfileForm


class HomeView(TemplateView):
    template_name="home.html"

    def get_context_data(self, **kwargs):
        context = super(HomeView, self).get_context_data(**kwargs)
        context['package_url'] = os.path.join(settings.MEDIA_URL, settings.CATALOGUE_PACKAGE)
        context['package_student_url'] = os.path.join(settings.MEDIA_URL, settings.CATALOGUE_PACKAGE_STUDENT)
        return context

class AvatarlessProfileEditView(ProfileEditView):
    form_class = AvatarlessEditProfileForm
