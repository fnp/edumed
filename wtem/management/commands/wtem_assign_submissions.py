from optparse import make_option

from django.core.management.base import BaseCommand, CommandError
from django.db.models import Count
from django.contrib.auth.models import User

from contact.models import Contact
from wtem.models import Submission, Attachment


class Command(BaseCommand):

    option_list = BaseCommand.option_list + (
        make_option('--with-attachments-only',
            action='store_true',
            dest='attachments_only',
            default=False,
            help='Take into account only submissions with attachments'),
        make_option('--without-attachments-only',
            action='store_true',
            dest='no_attachments_only',
            default=False,
            help='Take into account only submissions without attachments'),
        )

    def handle(self, *args, **options):

        limit_from = int(args[0])
        limit_to = int(args[1])
        examiner_names = args[2:]

        users = User.objects.filter(username__in = examiner_names)
        submissions_query = Submission.objects.annotate(examiners_count = Count('examiners'))

        submissions = submissions_query \
            .filter(examiners_count__lt=2).exclude(answers = None)
        
        with_attachment_ids = Attachment.objects.values_list('submission_id', flat=True).all()
        if options['attachments_only']:
            submissions = submissions.filter(id__in = with_attachment_ids)
        if options['no_attachments_only']:
            submissions = submissions.exclude(id__in = with_attachment_ids)

        for submission in submissions.order_by('id')[limit_from:limit_to]:
            submission.examiners.add(*users)
            submission.save()
            self.stdout.write('added to %s:%s' % (submission.id, submission.email))

        count_by_examiners = dict()
        for submission in submissions_query.all():
            count_by_examiners[submission.examiners_count] = \
                count_by_examiners.get(submission.examiners_count, 0) + 1
        self.stdout.write('%s' % count_by_examiners)
