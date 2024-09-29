# -*- coding: utf-8 -*-
from django.core.management.base import BaseCommand

from contact.models import Contact
from wtem.models import Submission


class Command(BaseCommand):

    def handle(self, *ids, **options):
        new = 0
        skipped = 0

        query = Contact.objects.filter(form_tag='wlem').order_by('-created_at')
        if ids:
            query = query.filter(pk__in=ids)

        for wlem_contact in query:
            if not Submission.objects.filter(email=wlem_contact.contact).exists():
                first_name, last_name = wlem_contact.body['nazwisko'].split()
                args = {
                    'email': wlem_contact.contact,
                    'first_name': first_name,
                    'last_name': last_name,
                }
                Submission.create(**args)
                new += 1
            else:
                self.stdout.write('skipping ' + wlem_contact.contact + ': already exists.')
                skipped += 1

        self.stdout.write('New: ' + str(new) + ', skipped: ' + str(skipped))
