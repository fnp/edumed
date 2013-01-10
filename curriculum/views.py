from django.db import models
from django.views.generic import DetailView, ListView
from django.utils.datastructures import SortedDict
from .models import Competence, Section, Level, CompetenceLevel


class CompetenceDetailView(DetailView):
    model = Competence


class CompetencesView(ListView):
    model = Competence

    def get_context_data(self, **kwargs):
        context = super(CompetencesView, self).get_context_data(**kwargs)
        context['levels'] = Level.objects.all()
        context['sections'] = Section.objects.all()

        errors = {}

        try:
            level = Level.objects.get(slug=self.request.GET.get('level'))
        except Level.DoesNotExist:
            level = None
        context['level'] = level

        comp_ids = set()
        for c in self.request.GET.getlist('c'):
            try:
                comp_ids.add(int(c))
            except ValueError:
                pass
        context['comp_ids'] = comp_ids
        sect_ids = set()
        for c in self.request.GET.getlist('s'):
            try:
                sect_ids.add(int(c))
            except ValueError:
                pass
        context['sect_ids'] = sect_ids

        if not (comp_ids or sect_ids):
            if level:
                errors["competences"] = "Please!"
        elif level is None:
            errors["level"] = "Please!"
        else:
            chosen_competences = SortedDict()
            for competence in Competence.objects.filter(
                    models.Q(pk__in=comp_ids) | models.Q(section__pk__in=sect_ids)):
                try:
                    competence.for_level_ = competence.for_level(level)
                except CompetenceLevel.DoesNotExist:
                    pass
                chosen_competences.setdefault(competence.section, []).append(competence)
            context['chosen_competences'] = chosen_competences

        context["errors"] = errors
        return context
