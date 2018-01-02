# -*- coding: utf-8 -*-

from optparse import make_option

from django.core.management.base import BaseCommand
from wtem.management.commands import send_mail
from django.template.loader import render_to_string

from stage2.models import Participant


class Command(BaseCommand):
    help = 'Sends personalized links to WTEM contestants'
    args = '<email_address1>, <email_address2>, ...'

    option_list = BaseCommand.option_list + (
        make_option(
            '--all',
            action='store_true',
            dest='all',
            default=False,
            help='Use all available participants'),
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
        self.stdout.write('No participants selected')

    def send_keys(self, *args, **options):
        sent = 0
        failed = 0

        participants = Participant.objects.all()
        if not options['force']:
            participants = participants.filter(key_sent=False)
        if len(args):
            participants = participants.filter(email__in=args)

        for participant in participants:
            assert len(participant.key) == 30

            try:
                self.send_key(participant)
            except Exception as e:
                failed += 1
                self.stdout.write('failed sending to: ' + participant.email + ' - ' + str(e))
            else:
                participant.key_sent = True
                participant.save()
                sent += 1
                self.stdout.write('key sent to: ' + participant.email)

        self.stdout.write('sent: ' + str(sent))

    def send_key(self, participant):
        self.stdout.write('>>> sending to ' + participant.email)
        send_mail(
            subject=u"II etap Olimpiady Cyfrowej – link do panelu",
            body=render_to_string('stage2/email_key.txt', {'participant': participant}),
            to=[participant.email])
