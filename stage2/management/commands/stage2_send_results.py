# -*- coding: utf-8 -*-
from collections import defaultdict
from decimal import Decimal
from optparse import make_option

from django.core.management.base import BaseCommand
from wtem.management.commands import send_mail
from django.utils import translation
from django.template.loader import render_to_string

from stage2.models import Participant


def get_participants():
    return sorted(Participant.objects.filter(complete_set=True), key=lambda s: -s.score())

minimum = Decimal('73.33')


class Command(BaseCommand):

    option_list = BaseCommand.option_list + (
        make_option(
            '--to-teachers',
            action='store_true',
            dest='to_teachers',
            default=False,
            help='Send emails to teachers'),
        make_option(
            '--to-students',
            action='store_true',
            dest='to_students',
            default=False,
            help='Send emails to students'),
        make_option(
            '--only-to',
            action='store',
            dest='only_to',
            default=None,
            help='Send email only to one address'),
    )

    def __init__(self):
        super(Command, self).__init__()
        self.sent = self.failed = None

    def handle(self, *args, **options):
        translation.activate('pl')
        for target in ['to_teachers', 'to_students']:
            if options[target]:
                self.sent = 0
                self.failed = 0
                getattr(self, 'handle_' + target)(*args, **options)

    def handle_to_students(self, *args, **options):
        self.stdout.write('>>> Sending results to students')
        subject = 'Wyniki II etapu Olimpiady Cyfrowej'

        for participant in get_participants():
            if options['only_to'] and participant.email != options['only_to']:
                continue
            final_result = participant.score()
            if final_result < minimum:
                template = 'results_student_failed.txt'
            else:
                template = 'results_student_passed.txt'
            message = render_to_string('stage2/' + template, dict(final_result=final_result))
            self.send_message(message, subject, participant.email)

        self.sum_up()

    def handle_to_teachers(self, *args, **options):
        self.stdout.write('>>> Sending results to teachers')
        subject = 'Wyniki II etapu Olimpiady Cyfrowej'

        participants_by_contact = defaultdict(list)

        for participant in get_participants():
            if options['only_to'] and participant.contact.contact != options['only_to']:
                continue
            participants_by_contact[participant.contact.contact].append(participant)

        for contact_email, participants in participants_by_contact.items():
            message = render_to_string('stage2/results_teacher.txt', dict(participants=participants))
            self.send_message(message, subject, contact_email)

        self.sum_up()

    def sum_up(self):        
        self.stdout.write('sent: %s, failed: %s' % (self.sent, self.failed))

    def send_message(self, message, subject, email):
        self.stdout.write('>>> sending results to %s' % email)
        try:
            send_mail(subject=subject, body=message, to=[email])
        except BaseException, e:
            self.failed += 1
            self.stdout.write('failed sending to: ' + email + ': ' + str(e))
        else:
            self.sent += 1
            self.stdout.write('message sent to: ' + email)
