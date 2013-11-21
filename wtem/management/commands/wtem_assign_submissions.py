from django.core.management.base import BaseCommand, CommandError
from django.db.models import Count
from django.contrib.auth.models import User

from contact.models import Contact
from wtem.models import Submission


class Command(BaseCommand):

    def handle(self, *args, **options):
        how_many = int(args[0])
        examiner_names = args[1:]

        users = User.objects.filter(username__in = examiner_names)
        submissions_query = Submission.objects.annotate(examiners_count = Count('examiners'))

        submissions = submissions_query \
            .filter(examiners_count__lt=2).exclude(answers = None)[0:how_many]

        for submission in submissions:
            submission.examiners.add(*users)
            submission.save()
            self.stdout.write('added to %s:%s' % (submission.id, submission.email))

        count_by_examiners = dict()
        for submission in submissions_query.all():
            count_by_examiners[submission.examiners_count] = \
                count_by_examiners.get(submission.examiners_count, 0) + 1
        self.stdout.write('%s' % count_by_examiners)
