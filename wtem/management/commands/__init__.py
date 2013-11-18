from django.core.mail import EmailMessage
from django.conf import settings

def send_mail(subject, body, to):
    if not isinstance(to, list):
        to = [to]

    reply_to = getattr(settings, 'WTEM_REPLY_TO', None)
    headers = dict()
    if reply_to:
        headers['Reply-To'] = reply_to

    email = EmailMessage(subject, body,
        getattr(settings, 'WTEM_FROM', 'edukacjamedialna@nowoczesnapolska.org.pl'),
        to, headers = headers)
    email.send(fail_silently = False)