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

        from catalogue.management.commands.importlessons import Command
        from django.conf import settings
        import os.path

        attachments = Command.all_attachments(os.path.join(settings.MEDIA_ROOT, 'catalogue', 'attachments'))

        for lesson in Lesson.objects.all():
            print
            print 'Republishing: %s' % lesson.slug
            lesson.republish(repackage_level=False, attachments=attachments)

        print 'Rebuilding levels...'
        for level in Level.objects.all():
            level.build_packages()
