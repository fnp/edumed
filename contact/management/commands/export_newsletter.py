# -*- coding: utf-8 -*-
# This file is part of EduMed, licensed under GNU Affero GPLv3 or later.
# Copyright © Fundacja Nowoczesna Polska. See NOTICE for more information.
#
from django.core.management.base import BaseCommand

from contact.models import Contact
from edumed import contact_forms

FORMS = (
    contact_forms.OlimpiadaForm,
)


class Command(BaseCommand):
    help = 'Export contacts for newsletter.'

    def handle(self, **options):
        addresses = set(self.get_addresses())
        for address in addresses:
            print address

    def get_addresses(self):
        for form in FORMS:
            tags = [form.form_tag] + form.old_form_tags
            contacts = Contact.objects.filter(form_tag__in=tags)
            for contact in contacts:
                if contact.body.get(form.mailing_field):
                    yield contact.contact
