from django.core.management.base import BaseCommand, CommandError

from contact.models import Contact
from wtem.models import Submission


class Command(BaseCommand):
    
    def handle(self, *args, **options):
        new = 0
        skipped = 0

        for wtem_contact in Contact.objects.filter(form_tag = 'wtem'):
            for student in wtem_contact.body['student']:
                if not Submission.objects.filter(email = student['email']).exists():
                    args = dict()
                    for attr in ['first_name', 'last_name', 'email']:
                        args[attr] = student[attr]
                    args['contact'] = wtem_contact
                    Submission.create(**args)
                    new += 1
                else:
                    self.stdout.write('skipping ' + student['email'] + ': already exists.')
                    skipped += 1

        self.stdout.write('New: ' + str(new) + ', skipped: ' + str(skipped))
