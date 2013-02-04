from django import template
from ..models import Competence

register = template.Library()


@register.filter
def find_competence(text):
    try:
        return Competence.from_text(text)
    except:
        return None

@register.filter
def url_for_level(comp, level):
    try:
        return comp.for_level(level).get_absolute_url()
    except:
        return comp.get_absolute_url()

