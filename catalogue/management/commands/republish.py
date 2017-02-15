# -*- coding: utf-8 -*-
# This file is part of EduMed, licensed under GNU Affero GPLv3 or later.
# Copyright © Fundacja Nowoczesna Polska. See NOTICE for more information.
#
from optparse import make_option

import librarian
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = 'Republishes all lessons.'

    option_list = BaseCommand.option_list + (
        make_option('--exclude', dest='exclude', metavar="PATH", default=None,
                    help='PATH to file with excluded lesson slugs.'),
        make_option('--ignore-incomplete', action='store_true', dest='ignore_incomplete', default=False,
                    help='Attachments dir path.'),
        make_option('--dont-repackage', action='store_false', dest='repackage', default=True,
                    help='Don\'t refresh level packages.'),
    )

    def handle(self, **options):
        from catalogue.models import Lesson
        from curriculum.models import Level

        lessons = Lesson.objects.order_by('slug')

        if options.get('exclude'):
            slugs = [line.strip() for line in open(options['exclude'])]
            lessons = lessons.exclude(slug__in=slugs)

        for lesson in lessons:
            print
            print 'Republishing: %s' % lesson.slug
            try:
                lesson.republish(repackage_level=False)
            except librarian.ParseError as e:
                print '!!!!!! PARSE ERROR !!!!!!'
                print e

        print 'Rebuilding levels...'
        for level in Level.objects.all():
            print level.name
            level.build_packages()
