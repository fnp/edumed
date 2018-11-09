# -*- coding: utf-8 -*-
from django.db import models
from django.db.models import permalink
from django.utils.translation import ugettext_lazy as _
from jsonfield import JSONField
from . import app_settings


class Contact(models.Model):
    created_at = models.DateTimeField(_('submission date'), auto_now_add=True)
    ip = models.IPAddressField(_('IP address'))
    contact = models.CharField(_('contact'), max_length=128)
    form_tag = models.CharField(_('form'), max_length=32, db_index=True)
    body = JSONField(_('body'))

    @staticmethod
    def pretty_print(value, for_html=False):
        if type(value) in (tuple, list, dict):
            import yaml
            value = yaml.safe_dump(value, allow_unicode=True, default_flow_style=False)
            if for_html:
                from django.utils.encoding import smart_unicode
                value = smart_unicode(value).replace(u" ", unichr(160))
        return value

    class Meta:
        ordering = ('-created_at',)
        verbose_name = _('submitted form')
        verbose_name_plural = _('submitted forms')

    def __unicode__(self):
        return unicode(self.created_at)

    def get_form_class(self):
        from contact.forms import contact_forms
        return contact_forms.get(self.form_tag)

    def get_update_form_class(self):
        from contact.forms import update_forms
        return update_forms.get(self.form_tag, self.get_form_class())

    @permalink
    def update_url(self):
        form_class = self.get_update_form_class()
        confirmation = form_class.confirmation_class.objects.get(contact=self)
        return 'edit_form', [], {'form_tag': self.form_tag, 'contact_id': self.id, 'key': confirmation.key}

    def send_confirmation(self, context=None, form=None):
        from django.template.loader import render_to_string
        from django.core.mail import send_mail
        from django.contrib.sites.models import Site
        if not form:
            form_class = self.get_form_class()
            form = form_class()
        dictionary = form.get_dictionary(self)
        mail_subject = render_to_string([
            'contact/%s/mail_subject.txt' % self.form_tag,
            'contact/mail_subject.txt',
        ], dictionary, context).strip()
        if form.result_page:
            mail_body = render_to_string(
                'contact/%s/results_email.txt' % self.form_tag,
                {
                    'contact': self,
                    'results': form.results(self),
                }, context)
        else:
            mail_body = render_to_string([
                'contact/%s/mail_body.txt' % self.form_tag,
                'contact/mail_body.txt',
            ], dictionary, context)
        site = Site.objects.get_current()
        send_mail(mail_subject, mail_body, 'no-reply@%s' % site.domain, [self.contact], fail_silently=True)


class Attachment(models.Model):
    contact = models.ForeignKey(Contact)
    tag = models.CharField(max_length=64)
    file = models.FileField(upload_to='contact/attachment')

    @models.permalink
    def get_absolute_url(self):
        return 'contact_attachment', [self.contact_id, self.tag]


__import__(app_settings.FORMS_MODULE)
