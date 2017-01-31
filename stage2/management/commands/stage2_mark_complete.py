# -*- coding: utf-8 -*-
from django.core.management.base import BaseCommand

from stage2.models import Participant, Assignment


class Command(BaseCommand):

    def handle(self, **options):
        assignment_count = Assignment.objects.count()
        for participant in Participant.objects.all():
            if participant.answer_set.count() == assignment_count:
                participant.complete_set = True
                participant.save()
