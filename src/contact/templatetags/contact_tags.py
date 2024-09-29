# -*- coding: utf-8 -*-
from django.template import Library

from contact.forms import contact_forms
from contact.models import Contact

register = Library()


@register.filter
def pretty_print(value):
    return Contact.pretty_print(value)


@register.filter
def is_enabled(form_tag):
    form_class = contact_forms.get(form_tag)
    if form_class:
        return not getattr(form_class, 'disabled', False)
    else:
        return False
