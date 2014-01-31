import os.path
from django.conf import settings
from django.views.generic import DetailView, ListView
from .models import Lesson, Section
from curriculum.models import Level
from publishers.models import Publisher


class LessonListView(ListView):
    queryset = Level.objects.exclude(lesson=None)
    template_name = "catalogue/lesson_list.html"

    def get_context_data(self, **kwargs):
        context = super(LessonListView, self).get_context_data(**kwargs)
        context['appendix'] = Lesson.objects.filter(type='appendix')
        return context


class LessonView(DetailView):
    model = Lesson

    def get_template_names(self):
        return [
            'catalogue/lesson/%s/lesson_detail.html' % self.object.type,
            'catalogue/lesson/lesson_detail.html',
        ]

    def get_context_data(self, **kwargs):
        context = super(LessonView, self).get_context_data(**kwargs)
        try:
            context['publisher'] = Publisher.objects.get(
                name=context['object'].dc.get('publisher', '').strip())
        except:
            pass
        return context
