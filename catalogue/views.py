import os.path
from django.conf import settings
from django.views.generic import DetailView, ListView
from .models import Section

class SectionView(ListView):
    model = Section

    def get_context_data(self, **kwargs):
        context = super(SectionView, self).get_context_data(**kwargs)
        context['package_url'] = os.path.join(settings.MEDIA_URL, settings.CATALOGUE_PACKAGE)
        context['package_student_url'] = os.path.join(settings.MEDIA_URL, settings.CATALOGUE_PACKAGE_STUDENT)
        return context
