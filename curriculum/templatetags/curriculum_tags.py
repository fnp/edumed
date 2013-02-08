from django import template
from django.utils.datastructures import SortedDict
from ..models import Competence, Curriculum

register = template.Library()


@register.inclusion_tag("curriculum/snippets/competence.html")
def competence(texts):
    try:
        comps = [Competence.from_text(text) for text in texts]
    except:
        return {'texts': texts}
    return {
        'comps': comps,
    }

@register.inclusion_tag("curriculum/snippets/curriculum.html")
def curriculum(identifiers):
    try:
        currs = [Curriculum.objects.get(identifier=identifier)
                    for identifier in identifiers]
    except Curriculum.DoesNotExist:
        return {'identifiers': identifiers}

    currset = SortedDict()
    for curr in currs:
        k = curr.course, curr.level
        if k not in currset:
            currset[k] = SortedDict()
        typename = Curriculum.TYPES[curr.type]
        if typename not in currset[k]:
            currset[k][typename] = []
        currset[k][typename].append(curr)

    return {
        'currset': currset,
    }
    

@register.filter
def url_for_level(comp, level):
    try:
        return comp.for_level(level).get_absolute_url()
    except:
        return comp.get_absolute_url()

