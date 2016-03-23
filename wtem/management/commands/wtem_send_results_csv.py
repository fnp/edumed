# -*- coding: utf-8 -*-

from optparse import make_option

from django.core.management.base import BaseCommand
from django.template.loader import render_to_string
from django.utils import translation

from wtem.management.commands import send_mail
from wtem.models import Submission


def get_submissions():
    return sorted(Submission.objects.exclude(answers=None).all(), key=lambda s: -s.final_result)

minimum = 52


class Command(BaseCommand):
    args = 'csv_filename'

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
            help='Send emails only to listed addresses'),
    )

    def handle(self, csv_filename, *args, **options):
        translation.activate('pl')
        self.results = [line.decode('utf-8').strip('\n').split(',') for line in open(csv_filename)]
        for target in ['to_teachers', 'to_students']:
            if options[target]:
                self.sent = 0
                self.failed = 0
                getattr(self, 'handle_' + target)(*args, **options)

    def handle_to_students(self, *args, **options):
        self.stdout.write('>>> Sending results to students')
        subject = 'Wyniki I etapu Wielkiego Turnieju Edukacji Medialnej'

        for result in self.results:
            if options['only_to'] and result[1] != options['only_to']:
                continue
            final_result = result[4]
            if result[5] != 'TAK':
                template = 'results_student_failed.txt'
            else:
                template = 'results_student_passed.txt'
            message = render_to_string('wtem/' + template, dict(final_result=final_result))
            self.send_message(message, subject, result[1])

        self.sum_up()

    def handle_to_teachers(self, *args, **options):
        self.stdout.write('>>> Sending results to teachers')
        subject = 'Wyniki I etapu Wielkiego Turnieju Edukacji Medialnej'

        submissions_by_contact = dict()

        from decimal import Decimal, InvalidOperation

        def dec_or_0(s):
            try:
                return Decimal(s)
            except InvalidOperation:
                return Decimal(0)

        for result in sorted(self.results, key=lambda r: dec_or_0(r[4]), reverse=True):
            if options['only_to'] and result[3] != options['only_to']:
                continue
            submissions_by_contact.setdefault(result[3], []).append({
                'first_name': result[0].split()[0],
                'last_name': result[0].split()[1],
                'final_result': result[4],
            })

        for email, submissions in submissions_by_contact.items():
            # contact = Contact.objects.get(id=contact_id)
            message = render_to_string('wtem/results_teacher.txt', dict(submissions=submissions))
            self.send_message(message, subject, email)

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
