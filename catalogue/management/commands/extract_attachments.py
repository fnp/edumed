# -*- coding: utf-8 -*-
# This file is part of EduMed, licensed under GNU Affero GPLv3 or later.
# Copyright © Fundacja Nowoczesna Polska. See NOTICE for more information.
#
import errno
from optparse import make_option
import os
import shutil

from django.core.management.base import BaseCommand


def makedir(directory):
    try:
        os.makedirs(directory)
    except OSError as e:
        if e.errno != errno.EEXIST:
            raise


class Command(BaseCommand):
    help = 'Extracts attachments from given lessons.'

    option_list = BaseCommand.option_list + (
        make_option('--slugs', dest='slugs_path', metavar="PATH", default=None,
                    help='PATH to file with lesson slugs.'),
    )

    def handle(self, **options):
        from catalogue.models import Lesson

        lessons = Lesson.objects.order_by('slug')
        if options.get('slugs_path'):
            slugs = [line.strip() for line in open(options.get('slugs_path')) if line.strip()]
            lessons = lessons.filter(slug__in=slugs)

        for lesson in lessons:
            makedir('materialy/%s' % lesson.slug)
            for attachment in lesson.attachment_set.all():
                shutil.copy(attachment.file.path, 'materialy/%s/%s.%s' % (lesson.slug, attachment.slug, attachment.ext))

