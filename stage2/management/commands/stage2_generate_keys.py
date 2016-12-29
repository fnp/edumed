# -*- coding: utf-8 -*-
from django.core.management.base import BaseCommand

from stage2.models import Participant
from wtem.management.commands.wtem_send_results import minimum, get_submissions


class Command(BaseCommand):

    def handle(self, **options):
        new = 0
        skipped = 0
        for s in get_submissions():
            if s.final_result >= minimum:
                if not Participant.objects.filter(email=s.email).exists():
                    Participant.create(s.first_name, s.last_name, s.email, contact=s.contact)
                    new += 1
                else:
                    self.stdout.write('skipping ' + s.email + ': already exists.')
                    skipped += 1

        self.stdout.write('New: ' + str(new) + ', skipped: ' + str(skipped))
