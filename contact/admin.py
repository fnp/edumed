# -*- coding: utf-8 -*-
import csv

from django.contrib import admin
from django.utils.translation import ugettext as _
from django.utils.safestring import mark_safe
from django.conf.urls import patterns, url
from django.http import HttpResponse, Http404

from edumed.utils import UnicodeCSVWriter
from .forms import contact_forms, admin_list_width
from .models import Contact


class ContactAdminMeta(admin.ModelAdmin.__class__):
    def __getattr__(cls, name):
        if name.startswith('admin_list_'):
            return lambda self: ""
        raise AttributeError(name)


class ContactAdmin(admin.ModelAdmin):
    __metaclass__ = ContactAdminMeta
    date_hierarchy = 'created_at'
    list_display = ['created_at', 'contact', 'form_tag'] + \
        ["admin_list_%d" % i for i in range(admin_list_width)]
    fields = ['form_tag', 'created_at', 'contact', 'ip']
    readonly_fields = ['form_tag', 'created_at', 'contact', 'ip']
    list_filter = ['form_tag']

    @staticmethod
    def admin_list(obj, nr):
        try:
            field_name = contact_forms[obj.form_tag].admin_list[nr]
        except BaseException:
            return ''
        else:
            return Contact.pretty_print(obj.body.get(field_name, ''), for_html=True)

    def __getattr__(self, name):
        if name.startswith('admin_list_'):
            nr = int(name[len('admin_list_'):])
            return lambda obj: self.admin_list(obj, nr)
        raise AttributeError(name)

    def change_view(self, request, object_id, form_url='', extra_context=None):
        if object_id:
            try:
                instance = Contact.objects.get(pk=object_id)
                assert isinstance(instance.body, dict)
            except (Contact.DoesNotExist, AssertionError):
                pass
            else:
                # Create readonly fields from the body JSON.
                body_fields = ['body__%s' % k for k in instance.body.keys()]
                attachments = list(instance.attachment_set.all())
                body_fields += ['body__%s' % a.tag for a in attachments]
                self.readonly_fields.extend(body_fields)

                # Find the original form.
                try:
                    orig_fields = contact_forms[instance.form_tag]().fields
                except KeyError:
                    orig_fields = {}

                # Try to preserve the original order.
                admin_fields = []
                orig_keys = list(orig_fields.keys())
                while orig_keys:
                    key = orig_keys.pop(0)
                    key = "body__%s" % key
                    if key in body_fields:
                        admin_fields.append(key)
                        body_fields.remove(key)
                admin_fields.extend(body_fields)

                self.fieldsets = [
                    (None, {'fields': self.fields}),
                    (_('Body'), {'fields': admin_fields}),
                ]

                # Create field getters for fields and attachments.
                for k, v in instance.body.items():
                    f = (lambda v: lambda self: v)(Contact.pretty_print(v, for_html=True))
                    f.short_description = orig_fields[k].label if k in orig_fields else _(k)
                    setattr(self, "body__%s" % k, f)

                download_link = "<a href='%(url)s'>%(url)s</a>"
                for attachment in attachments:
                    k = attachment.tag
                    link = mark_safe(download_link % {
                            'url': attachment.get_absolute_url()})
                    f = (lambda v: lambda self: v)(link)
                    f.short_description = orig_fields[k].label if k in orig_fields else _(k)
                    setattr(self, "body__%s" % k, f)
        return super(ContactAdmin, self).change_view(
            request, object_id, form_url=form_url, extra_context=extra_context)

    def changelist_view(self, request, extra_context=None):
        context = dict()
        if 'form_tag' in request.GET:
            form = contact_forms.get(request.GET['form_tag'])
            context['extract_types'] = [
                {'slug': 'all', 'label': _('all')},
                {'slug': 'contacts', 'label': _('contacts')}]
            context['extract_types'] += [type for type in getattr(form, 'extract_types', [])]
        return super(ContactAdmin, self).changelist_view(request, extra_context=context)

    def get_urls(self):
        # urls = super(ContactAdmin, self).get_urls()
        return patterns(
            '',
            url(r'^extract/(?P<form_tag>[\w-]+)/(?P<extract_type_slug>[\w-]+)/$',
                self.admin_site.admin_view(extract_view), name='contact_extract')
        ) + super(ContactAdmin, self).get_urls()


def extract_view(request, form_tag, extract_type_slug):
    contacts_by_spec = dict()
    form = contact_forms.get(form_tag)
    if form is None and extract_type_slug not in ('contacts', 'all'):
        raise Http404

    q = Contact.objects.filter(form_tag=form_tag)
    at_year = request.GET.get('created_at__year')
    at_month = request.GET.get('created_at__month')
    if at_year:
        q = q.filter(created_at__year=at_year)
        if at_month:
            q = q.filter(created_at__month=at_month)

    # Segregate contacts by body key sets
    for contact in q.all():
        if extract_type_slug == 'contacts':
            keys = ['contact']
        elif extract_type_slug == 'all':
            keys = contact.body.keys() + ['contact']
        else:
            keys = form.get_extract_fields(contact, extract_type_slug)
        contacts_by_spec.setdefault(tuple(keys), []).append(contact)

    response = HttpResponse(content_type='text/csv')
    csv_writer = UnicodeCSVWriter(response)

    # Generate list for each body key set
    for keys, contacts in contacts_by_spec.items():
        csv_writer.writerow(keys)
        for contact in contacts:
            if extract_type_slug == 'contacts':
                records = [dict(contact=contact.contact)]
            elif extract_type_slug == 'all':
                records = [dict(contact=contact.contact, **contact.body)]
            else:
                records = form.get_extract_records(keys, contact, extract_type_slug)

            for record in records:
                for key in keys:
                    if key not in record:
                        record[key] = ''
                    if isinstance(record[key], bool):
                        record[key] = 'tak' if record[key] else 'nie'
                    if isinstance(record[key], (list, tuple)):
                        record[key] = ', '.join(record[key])

                csv_writer.writerow([record[key] for key in keys])
        csv_writer.writerow([])

    response['Content-Disposition'] = 'attachment; filename="kontakt.csv"'
    return response

admin.site.register(Contact, ContactAdmin)
