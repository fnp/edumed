from .models import Competence, Section, Level


from django.views.generic import DetailView, ListView

class CompetenceDetailView(DetailView):
    model = Competence

class CompetencesView(ListView):
    model = Competence

    def get_context_data(self, **kwargs):
        print 'kwargs', kwargs
        context = super(CompetencesView, self).get_context_data(**kwargs)

        queryset = self.get_queryset()

        return context
        
