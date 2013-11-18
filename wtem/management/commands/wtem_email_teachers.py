# -*- coding: utf-8 -*-

import sys
from optparse import make_option

from django.core.management.base import BaseCommand, CommandError
from django.conf import settings
from wtem.management.commands import send_mail
from django.template.loader import render_to_string

from contact.models import Contact


class Command(BaseCommand):
    def handle(self, *args, **options):
        sent = 0
        failed = 0

        query = Contact.objects.filter(form_tag = 'wtem').order_by('contact').distinct('contact')
        template_name = args[0]
        message = render_to_string('wtem/' + template_name + '.txt')
        subject = render_to_string('wtem/' + template_name + '_subject.txt')
        
        answer = raw_input('Send the following to %d teachers with subject "%s"\n\n %s\n\n?' % \
            (query.count(), subject.encode('utf8'), message.encode('utf8')))

        if answer == 'yes':
            for contact in query:
                try:
                    self.send_message(message, subject, contact.contact)
                except Exception as e:
                    failed += 1
                    self.stdout.write('failed sending to: ' + contact.contact + ' - ' + str(e))
                else:
                    sent += 1
                    self.stdout.write('message sent to: ' + contact.contact)

        self.stdout.write('sent: %s, failed: %s' % (sent, failed))

    def send_message(self, message, subject, email):
        self.stdout.write('>>> sending to %s' % email)
        send_mail(
            subject = subject,
            body = message,
            to = [email]
        )

