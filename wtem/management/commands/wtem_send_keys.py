# -*- coding: utf-8 -*-

from optparse import make_option

from django.core.management.base import BaseCommand
from django.conf import settings
from wtem.management.commands import send_mail
from django.template.loader import render_to_string

from wtem.models import Submission, DEBUG_KEY


class Command(BaseCommand):
    help = 'Sends personalized links to WTEM contestants'
    args = '<email_address1>, <email_address2>, ...'

    option_list = BaseCommand.option_list + (
        make_option(
            '--all',
            action='store_true',
            dest='all',
            default=False,
            help='Use all available submissions'),
        make_option(
            '--force',
            action='store_true',
            dest='force',
            default=False,
            help='Force sending key even if one was already sent')
        )

    def handle(self, *args, **options):
        if len(args) or options['all']:
            return self.send_keys(*args, **options)
        self.stdout.write('No submissions selected')

    def send_keys(self, *args, **options):
        sent = 0
        failed = 0

        submissions = Submission.objects.all()
        if not options['force']:
            submissions = submissions.filter(key_sent=False)
        if len(args):
            submissions = submissions.filter(email__in=args)

        for submission in submissions:
            assert len(submission.key) == 30 or (settings.DEBUG and submission.key == DEBUG_KEY)

            try:
                self.send_key(submission)
            except Exception as e:
                failed += 1
                self.stdout.write('failed sending to: ' + submission.email + ' - ' + repr(e))
            else:
                submission.key_sent = True
                submission.save()
                sent += 1
                self.stdout.write('key sent to: ' + submission.email)

        self.stdout.write('sent: ' + str(sent))

    def send_key(self, submission):
        self.stdout.write('>>> sending to ' + submission.email)
        send_mail(
            subject="Olimpiada Cyfrowa - Twój link do zadań I etapu",
            body=render_to_string('wtem/email_key.txt', dict(submission=submission)),
            to=[submission.email])
