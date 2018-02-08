# -*- coding: utf-8 -*-
from decimal import Decimal

from django import forms
from django.conf import settings
from django.template.defaultfilters import filesizeformat
from django.utils.safestring import mark_safe

from stage2.models import Attachment, Mark, FieldOptionSet, FieldOption


class AttachmentForm(forms.ModelForm):
    assignment_id = forms.CharField(widget=forms.HiddenInput)

    class Meta:
        model = Attachment
        fields = ['file']

    def __init__(self, assignment, file_no, label, extensions=None, *args, **kwargs):
        prefix = 'att%s-%s' % (assignment.id, file_no)
        super(AttachmentForm, self).__init__(*args, prefix=prefix, **kwargs)
        self.fields['assignment_id'].initial = assignment.id
        self.fields['file'].label = label
        if extensions:
            self.fields['file'].widget.attrs = {'data-ext': '|'.join(extensions)}
        self.extensions = extensions

    def clean_file(self):
        file = self.cleaned_data['file']
        if file.size > settings.MAX_UPLOAD_SIZE:
            raise forms.ValidationError(
                'Please keep filesize under %s. Current filesize: %s' % (
                    filesizeformat(settings.MAX_UPLOAD_SIZE), filesizeformat(file.size)))
        if self.extensions and ('.' not in file.name or file.name.rsplit('.', 1)[1].lower() not in self.extensions):
            raise forms.ValidationError('Incorrect extension, should be one of: %s' % ', '.join(self.extensions))
        return file


class AssignmentFieldForm(forms.Form):
    value = forms.CharField(required=False)
    assignment_id = forms.CharField(widget=forms.HiddenInput)

    def __init__(self, label, field_no, options, answer, *args, **kwargs):
        prefix = 'field%s-%s' % (answer.id, field_no)
        super(AssignmentFieldForm, self).__init__(prefix=prefix, *args, **kwargs)
        self.answer = answer
        self.label = label
        self.fields['value'].label = label
        self.type = options['type']
        self.fields['assignment_id'].initial = answer.assignment.id
        if self.type == 'options':
            option_set = FieldOptionSet.objects.get(name=options['option_set'])
            self.fields['value'].widget = forms.Select(choices=option_set.choices(answer))
            options = answer.fieldoption_set.all()
            if options:
                self.fields['value'].initial = options.get().id
        else:
            value = answer.field_values.get(label)
            self.fields['value'].initial = value or ''

    def clean_value(self):
        if self.type == 'options':
            value = self.cleaned_data['value']
            if value:
                try:
                    option = FieldOption.objects.get(id=int(value))
                except (FieldOption.DoesNotExist, ValueError):
                    raise forms.ValidationError(u'Nieprawidłowa wartość.')
                if option.answer != self.answer and option.answer is not None:
                    raise forms.ValidationError(u'Ta opcja została już wybrana przez kogoś innego.')
                return option
        return self.cleaned_data['value']

    def save(self):
        value = self.cleaned_data['value']
        if self.type == 'options':
            option = value
            if option:
                if option.answer != self.answer:
                    # not thread-safe :/
                    assert not option.answer
                    for opt in self.answer.fieldoption_set.all():
                        opt.answer = None
                        opt.save()
                    option.answer = self.answer
                    option.save()
            else:
                for opt in self.answer.fieldoption_set.all():
                    opt.answer = None
                    opt.save()
        else:
            self.answer.field_values[self.label] = value
            self.answer.save()


class MarkForm(forms.ModelForm):
    answer_id = forms.CharField(widget=forms.HiddenInput)

    class Meta:
        model = Mark
        fields = ['points']
        widgets = {
            'points': forms.TextInput(attrs={'type': 'number', 'min': 0, 'step': '0.5'})
        }

    def __init__(self, answer, criterion, *args, **kwargs):
        super(MarkForm, self).__init__(*args, **kwargs)
        self.fields['answer_id'].initial = answer.id
        points_field = self.fields['points']
        points_field.label = mark_safe(criterion.form_label())
        points_field.help_text = '(max %s)' % criterion.max_points
        points_field.min_value = Decimal(0)
        points_field.max_value = Decimal(criterion.max_points)
        points_field.widget.attrs['max'] = criterion.max_points
