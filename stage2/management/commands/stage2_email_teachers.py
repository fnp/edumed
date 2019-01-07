# -*- coding: utf-8 -*-

from django.core.management.base import BaseCommand
from django.template.loader import render_to_string

from stage2.models import Participant
from wtem.management.commands import send_mail


class Command(BaseCommand):
    def handle(self, *args, **options):
        sent = 0
        failed = 0

        query = Participant.objects.exclude(contact=None).order_by('contact__contact').distinct('contact__contact')\
            .values_list('contact__contact', flat=True)
        template_name = args[0]
        message = render_to_string('stage2/' + template_name + '.txt')
        subject = render_to_string('stage2/' + template_name + '_subject.txt')
        
        answer = raw_input(
            'Send the following to %d teachers with subject "%s"\n\n %s\n\n?' %
            (query.count(), subject.encode('utf8'), message.encode('utf8')))

        if answer == 'yes':
            for contact in query:
                try:
                    self.send_message(message, subject, contact)
                except Exception as e:
                    failed += 1
                    self.stdout.write('failed sending to: ' + contact + ' - ' + str(e))
                else:
                    sent += 1
                    self.stdout.write('message sent to: ' + contact)

        self.stdout.write('sent: %s, failed: %s' % (sent, failed))

    def send_message(self, message, subject, email):
        self.stdout.write('>>> sending to %s' % email)
        send_mail(subject=subject, body=message, to=[email])

