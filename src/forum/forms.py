# -*- coding: utf-8 -*-
from django import forms
from django.forms.models import ModelChoiceIterator
from django.utils.translation import ugettext as _
import pybb.forms

from catalogue.models import Lesson


class GroupedModelChoiceIterator(ModelChoiceIterator):
    def __init__(self, field):
        super(GroupedModelChoiceIterator, self).__init__(field)
        self.queryset = self.field.grouping_model.objects
        self.items_queryset = self.field.queryset
    
    def choice(self, obj):
        items_query = self.items_queryset.filter(**{self.field.grouping_fk_field: obj})
        items = [super(GroupedModelChoiceIterator, self).choice(item) for item in items_query.all()]
        return unicode(obj), items


class GroupedModelChoiceField(forms.ModelChoiceField):
    
    def __init__(self, queryset, grouping_fk_field, **kwargs):
        self.grouping_fk_field = grouping_fk_field
        self.grouping_model = queryset.model._meta.get_field(grouping_fk_field).rel.to
        super(GroupedModelChoiceField, self).__init__(queryset, **kwargs)

    def _get_choices(self):
        toret = super(GroupedModelChoiceField, self)._get_choices()
        if isinstance(toret, ModelChoiceIterator):
            toret = GroupedModelChoiceIterator(self)
        return toret

    choices = property(_get_choices, forms.ModelChoiceField.choices.fset)


class PostForm(pybb.forms.PostForm):
    lesson = GroupedModelChoiceField(
        label=_('Related lesson'), queryset=Lesson.objects.all(),
        grouping_fk_field='section', required=False)
