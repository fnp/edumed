# -*- coding: utf-8 -*-
# This file is part of EduMed, licensed under GNU Affero GPLv3 or later.
# Copyright © Fundacja Nowoczesna Polska. See NOTICE for more information.
#
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = 'Republishes all lessons.'

    def handle(self, **options):
        from catalogue.models import Lesson
        from curriculum.models import Level

        for lesson in Lesson.objects.all():
            print 'Republishing: %s' % lesson.title
            lesson.republish(repackage_level=False)

        print 'Rebuilding levels...'
        for level in Level.objects.all():
            level.build_packages()
