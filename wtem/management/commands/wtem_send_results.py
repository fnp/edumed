# -*- coding: utf-8 -*-

from optparse import make_option

from django.core.management.base import BaseCommand
from django.conf import settings
from wtem.management.commands import send_mail
from django.utils import translation
from django.template.loader import render_to_string

from contact.models import Contact
from wtem.models import Submission


def get_submissions():
    return Submission.objects.exclude(answers = None).all()

minimum = 55

class Command(BaseCommand):

    option_list = BaseCommand.option_list + (
        make_option('--to-teachers',
            action='store_true',
            dest='to_teachers',
            default=False,
            help='Send emails to teachers'),
        make_option('--to-students',
            action='store_true',
            dest='to_students',
            default=False,
            help='Send emails to students'),
        make_option('--only-to',
            action='store',
            dest='only_to',
            default=None,
            help='Send emails to students'),
    )

    def handle(self, *args, **options):
        translation.activate('pl')
        for target in ['to_teachers', 'to_students']:
            if options[target]:
                self.sent = 0
                self.failed = 0
                getattr(self, 'handle_' + target)(*args, **options)

    def handle_to_students(self, *args, **options):
        self.stdout.write('>>> Sending results to students')
        subject = 'Wyniki I etapu Wielkiego Turnieju Edukacji Medialnej'

        for submission in get_submissions():
            if options['only_to'] and submission.email != options['only_to']:
                continue
            final_result = submission.final_result
            if final_result < minimum:
                template = 'results_student_failed.txt'
            else:
                template = 'results_student_passed.txt'
            message = render_to_string('wtem/' + template, dict(final_result = submission.final_result))
            self.send_message(message, subject, submission.email)

        self.sum_up()

    def handle_to_teachers(self, *args, **options):
        self.stdout.write('>>> Sending results to teachers')
        subject = 'Wyniki I etapu Wielkiego Turnieju Edukacji Medialnej'
        failed = sent = 0

        submissions_by_contact = dict()

        for submission in get_submissions():
            if options['only_to'] and submission.contact.contact != options['only_to']:
                continue
            submissions_by_contact.setdefault(submission.contact.id, []).append(submission)

        for contact_id, submissions in submissions_by_contact.items():
            contact = Contact.objects.get(id=contact_id)
            message = render_to_string('wtem/results_teacher.txt', dict(submissions = submissions))
            self.send_message(message, subject, contact.contact)

        self.sum_up()

    def sum_up(self):        
        self.stdout.write('sent: %s, failed: %s' % (self.sent, self.failed))

    def send_message(self, message, subject, email):
        self.stdout.write('>>> sending results to %s' % email)
        try:
            send_mail(
                subject = subject,
                body = message,
                to = [email]
            )
        except:
            self.failed += 1
            self.stdout.write('failed sending to: ' + email + ': ' + str(e))
        else:
            self.sent += 1
            self.stdout.write('message sent to: ' + email)


