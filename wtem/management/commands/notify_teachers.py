# -*- coding: utf-8 -*-
from datetime import timedelta
from django.core.management.base import BaseCommand
from django.template.loader import render_to_string
from django.utils import timezone

from contact.models import Contact
from wtem.management.commands import send_mail
from wtem.models import Confirmation


THRESHOLD = 0

AFTER_DEADLINE = True


class Command(BaseCommand):
    def handle(self, *args, **options):
        sent = 0
        failed = 0

        query = Contact.objects.filter(form_tag='olimpiada').order_by('contact').distinct('contact')
        template_name = 'notify_unconfirmed'
        message_template = 'wtem/' + template_name + ('_after' if AFTER_DEADLINE else '') + '.txt'
        subject = render_to_string('wtem/' + template_name + '_subject.txt')

        threshold = timezone.now() - timedelta(THRESHOLD)

        for contact in query:
            unconfirmed = []
            contacts = []
            for similar_contact in Contact.objects.filter(contact=contact.contact, form_tag=contact.form_tag):
                contact_emails = [s['email'] for s in similar_contact.body.get('student', [])]
                new_unconfirmed = list(Confirmation.objects.filter(
                    contact=similar_contact, confirmed=False, contact__created_at__lt=threshold,
                    email__in=contact_emails))
                unconfirmed += new_unconfirmed
                if new_unconfirmed:
                    contacts.append(similar_contact)
            if not unconfirmed:
                continue
            message = render_to_string(message_template, {'unconfirmed': unconfirmed, 'contacts': contacts})
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
