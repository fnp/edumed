# -*- coding: utf-8 -*-

from django.core.management.base import BaseCommand
from django.template.loader import render_to_string

from contact.models import Contact
from wtem.management.commands import send_mail


class Command(BaseCommand):
    def handle(self, *args, **options):
        sent = 0
        failed = 0

        contacts = Contact.objects.filter(form_tag='olimpiada').exclude(contact=None).order_by('contact')\
            .distinct('contact')
        template_name = args[0]
        emails = args[1:]
        if emails:
            contacts = contacts.filter(contact__in=emails)
        message = render_to_string('wtem/' + template_name + '.txt')
        subject = render_to_string('wtem/' + template_name + '_subject.txt')
        
        answer = raw_input(
            'Send the following to %d teachers with subject "%s"\n\n%s\n\n?' %
            (contacts.count(), subject.encode('utf8'), message.encode('utf8')))

        if answer == 'yes':
            for contact in contacts:
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
        send_mail(subject=subject, body=message, to=[email])

