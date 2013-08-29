from django import forms
from django.utils.translation import ugettext as _
import pybb.forms

from catalogue.models import Lesson


class PostForm(pybb.forms.PostForm):
    lesson = forms.ModelChoiceField(label = _('Related lesson'), queryset = Lesson.objects.all())
    