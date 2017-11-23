# -*- coding: utf-8 -*-
from django.core.management.base import BaseCommand

from wtem.models import Submission, Confirmation


class Command(BaseCommand):

    def handle(self, **options):
        new = 0
        skipped = 0

        emails = list(Submission.objects.values_list('email', flat=True))
        for confirmation in Confirmation.objects.exclude(email__in=emails):
            args = {}
            for attr in ['first_name', 'last_name', 'email', 'contact']:
                args[attr] = getattr(confirmation, attr)
            Submission.create(**args)
            new += 1

        self.stdout.write('New: ' + str(new) + ', skipped: ' + str(skipped))
