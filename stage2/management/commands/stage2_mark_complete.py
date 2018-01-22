# -*- coding: utf-8 -*-
from django.core.management.base import BaseCommand

from stage2.models import Participant, Assignment


class Command(BaseCommand):

    def handle(self, **options):
        assignment_count = Assignment.objects.count()
        for participant in Participant.objects.all():
            answers = participant.answer_set.all()
            if len(answers) == assignment_count and all(answer.is_complete() for answer in answers):
                participant.complete_set = True
                participant.save()
