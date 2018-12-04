# -*- coding: utf-8 -*-
import os

from django.contrib.sites.models import Site
from django.core.exceptions import ValidationError
from django.core.files.uploadedfile import UploadedFile
from django.core.mail import send_mail, mail_managers
from django.core.validators import validate_email
from django import forms
from django.db.models.fields.files import FieldFile
from django.template.loader import render_to_string
from django.template import RequestContext
from django.utils.translation import ugettext_lazy as _

from . import mailing


contact_forms = {}
update_forms = {}
admin_list_width = 0


class ContactFormMeta(forms.Form.__class__):
    def __new__(cls, name, bases, attrs):
        global admin_list_width
        model = super(ContactFormMeta, cls).__new__(cls, name, bases, attrs)
        if model.form_tag:
            if model.form_type == 'create':
                assert model.form_tag not in contact_forms, 'Duplicate form_tag.'
                if model.admin_list:
                    admin_list_width = max(admin_list_width, len(model.admin_list))
                contact_forms[model.form_tag] = model
            elif model.form_type == 'update':
                assert model.form_tag not in update_forms, 'Duplicate form_tag.'
                update_forms[model.form_tag] = model
        return model


class ContactForm(forms.Form):
    """Subclass and define some fields."""
    __metaclass__ = ContactFormMeta

    form_tag = None
    form_type = 'create'
    updatable = False
    old_form_tags = []
    form_title = _('Contact form')
    submit_label = _('Submit')
    admin_list = None
    result_page = False
    mailing_field = None
    mailing = False
    data_processing = None
    form_formsets = {}

    disabled = False
    disabled_template = None

    required_css_class = 'required'
    contact = NotImplemented

    def __init__(self, data=None, files=None, *args, **kwargs):
        self.instance = kwargs.pop('instance', None)
        if self.instance and (data is not None or files is not None):
            for attachment in self.instance.attachment_set.all():
                if attachment.tag not in files:
                    files[attachment.tag] = attachment.file
        super(ContactForm, self).__init__(data, files, *args, **kwargs)
        if not self.is_bound and self.instance:
            self.fields['contact'].initial = self.instance.contact
            body = self.instance.body
            for field, value in body.iteritems():
                if field in self.fields:
                    self.fields[field].initial = value
            for attachment in self.instance.attachment_set.all():
                self.fields[attachment.tag].initial = attachment

    def get_dictionary(self, contact):
        site = Site.objects.get_current()
        return {
            'form_tag': self.form_tag,
            'site_name': getattr(self, 'site_name', site.name),
            'site_domain': getattr(self, 'site_domain', site.domain),
            'contact': contact,
        }

    @classmethod
    def is_disabled(cls):
        # end_time = localtime_to_utc(datetime(*cls.ends_on)) if cls.ends_on else None
        # expired = end_time and end_time < timezone.now()
        return cls.disabled  # or expired

    def formset_initial(self, prefix):
        if not self.instance:
            return None
        return self.instance.body.get(prefix)

    def get_formsets(self, request=None):
        request_data = {'data': request.POST, 'files': request.FILES} if request else {}
        kwargs_instance = dict(request_data)
        kwargs_instance['instance'] = self.instance
        formsets = {}
        for prefix, formset_class in self.form_formsets.iteritems():
            if getattr(formset_class, 'takes_instance', False):
                kwargs = kwargs_instance
            else:
                kwargs = request_data
            formsets[prefix] = formset_class(
                prefix=prefix, initial=self.formset_initial(prefix), **kwargs)
        return formsets

    def save(self, request, formsets=None):
        from .models import Attachment, Contact
        body = {}
        for name, value in self.cleaned_data.items():
            if not isinstance(value, UploadedFile) and not isinstance(value, FieldFile) and name != 'contact':
                body[name] = value

        for formset in formsets or []:
            for f in formset.forms:
                sub_body = {}
                for name, value in f.cleaned_data.items():
                    if not isinstance(value, UploadedFile):
                        sub_body[name] = value
                if sub_body:
                    body.setdefault(f.form_tag, []).append(sub_body)

        if self.instance:
            contact = self.instance
            contact.body = body
            email_changed = contact.contact != self.cleaned_data['contact']
            contact.contact = self.cleaned_data['contact']
            assert contact.form_tag == self.form_tag
            contact.save()
        else:
            contact = Contact.objects.create(
                body=body,
                ip=request.META['REMOTE_ADDR'],
                contact=self.cleaned_data['contact'],
                form_tag=self.form_tag)
            contact.generate_key()
            contact.save()
            email_changed = True
        for name, value in self.cleaned_data.items():
            if isinstance(value, UploadedFile):
                for attachment in Attachment.objects.filter(contact=contact, tag=name):
                    os.remove(attachment.file.path)
                    attachment.delete()
                attachment = Attachment(contact=contact, tag=name)
                attachment.file.save(value.name, value)
                attachment.save()

        site = Site.objects.get_current()
        dictionary = self.get_dictionary(contact)
        context = RequestContext(request)
        mail_managers_subject = render_to_string([
                'contact/%s/mail_managers_subject.txt' % self.form_tag,
                'contact/mail_managers_subject.txt', 
            ], dictionary, context).strip()
        mail_managers_body = render_to_string([
                'contact/%s/mail_managers_body.txt' % self.form_tag,
                'contact/mail_managers_body.txt', 
            ], dictionary, context)
        mail_managers(mail_managers_subject, mail_managers_body, fail_silently=True)

        try:
            validate_email(contact.contact)
        except ValidationError:
            pass
        else:
            if not self.instance:
                mail_subject = render_to_string([
                        'contact/%s/mail_subject.txt' % self.form_tag,
                        'contact/mail_subject.txt',
                    ], dictionary, context).strip()
                if self.result_page:
                    mail_body = render_to_string(
                        'contact/%s/results_email.txt' % contact.form_tag,
                        {
                            'contact': contact,
                            'results': self.results(contact),
                        }, context)
                else:
                    mail_body = render_to_string([
                            'contact/%s/mail_body.txt' % self.form_tag,
                            'contact/mail_body.txt',
                        ], dictionary, context)
                send_mail(mail_subject, mail_body, 'no-reply@%s' % site.domain, [contact.contact], fail_silently=True)
            if email_changed and (self.mailing or (self.mailing_field and self.cleaned_data[self.mailing_field])):
                mailing.subscribe(contact.contact)

        return contact
