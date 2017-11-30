# -*- coding: utf-8 -*-

from optparse import make_option

from collections import defaultdict
from django.core.management.base import BaseCommand
from wtem.management.commands import send_mail
from django.utils import translation
from django.template.loader import render_to_string

from wtem.models import Submission


def get_submissions():
    return sorted(Submission.objects.exclude(answers=None), key=lambda s: -s.final_result)

minimum = 63.06


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
        make_option(
            '--dummy',
            action='store_true',
            dest='dummy',
            default=False,
            help='Print emails instead of sending them'),
    )

    def __init__(self):
        super(Command, self).__init__()
        self.sent = self.failed = None
        self.dummy = None

    def handle(self, *args, **options):
        translation.activate('pl')
        self.dummy = options['dummy']
        for target in ['to_teachers', 'to_students']:
            if options[target]:
                self.sent = 0
                self.failed = 0
                getattr(self, 'handle_' + target)(*args, **options)

    def handle_to_students(self, *args, **options):
        self.stdout.write('>>> Sending results to students')
        subject = 'Wyniki I etapu Olimpiady Cyfrowej'

        for submission in get_submissions():
            if options['only_to'] and submission.email != options['only_to']:
                continue
            final_result = submission.final_result
            if final_result < minimum:
                template = 'results_student_failed.txt'
            else:
                template = 'results_student_passed.txt'
            message = render_to_string('wtem/' + template, dict(final_result=round(submission.final_result, 2)))
            self.send_message(message, subject, submission.email)

        self.sum_up()

    def handle_to_teachers(self, *args, **options):
        self.stdout.write('>>> Sending results to teachers')
        subject = 'Wyniki I etapu Olimpiady Cyfrowej'

        submissions_by_contact = defaultdict(list)

        for submission in get_submissions():
            if options['only_to'] and submission.contact.contact != options['only_to']:
                continue
            submissions_by_contact[submission.contact.contact].append(submission)

        for contact_email, submissions in submissions_by_contact.items():
            message = render_to_string('wtem/results_teacher.txt', dict(submissions=submissions))
            self.send_message(message, subject, contact_email)

        self.sum_up()

    def sum_up(self):        
        self.stdout.write('sent: %s, failed: %s' % (self.sent, self.failed))

    def send_message(self, message, subject, email):
        self.stdout.write('>>> sending results to %s' % email)
        if self.dummy:
            self.stdout.write(message)
            self.sent += 1
            return
        try:
            send_mail(subject=subject, body=message, to=[email])
        except BaseException, e:
            self.failed += 1
            self.stdout.write('failed sending to: ' + email + ': ' + str(e))
        else:
            self.sent += 1
            self.stdout.write('message sent to: ' + email)
