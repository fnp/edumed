# -*- coding: utf-8 -*-
# This file is part of EduMed, licensed under GNU Affero GPLv3 or later.
# Copyright © Fundacja Nowoczesna Polska. See NOTICE for more information.
#
import os
from optparse import make_option
from django.conf import settings
from django.core.management.base import BaseCommand
from catalogue.models import Section
import zipfile


class Command(BaseCommand):
    option_list = BaseCommand.option_list + (
        make_option('-q', '--quiet', action='store_false', dest='verbose', default=True,
            help='Verbosity level; 0=minimal output, 1=normal output, 2=all output'),
    )
    help = 'Rebuilds downloadable packages.'

    def build_package(self, zippath, student, verbose):
        with open(zippath, 'w') as outf:
            zipf = zipfile.ZipFile(outf, 'w', zipfile.ZIP_STORED)
            
            for si, section in enumerate(Section.objects.all()):
                li = 1
                li_adv = 1
                for lesson in section.lesson_set.all():
                    advanced = lesson.level.slug == "liceum"
                    section_dir = "%d_%s%s" % (
                        si + 1, section.slug,
                        " (zaawansowane)" if advanced else "")
                    if lesson.type == 'course':
                        if advanced:
                            ind = li_adv
                            li_adv += 1
                        else:
                            ind = li
                            li += 1
                        prefix = "%s/%02d_%s/" % (
                                section_dir, ind, lesson.slug,
                            )
                    elif lesson.type == 'synthetic':
                        prefix = "%s/%s (synteza)/" % (
                                section_dir, lesson.slug)
                    else:
                        prefix = "%s/%s/" % (
                                section_dir, lesson.slug)
                    lesson.add_to_zip(zipf, student, prefix)
            zipf.close()

    def handle(self, **options):
        verbose = options.get('verbose')

        self.build_package(
            os.path.join(settings.MEDIA_ROOT, settings.CATALOGUE_PACKAGE), 
            False, verbose)
        self.build_package(
            os.path.join(settings.MEDIA_ROOT, settings.CATALOGUE_PACKAGE_STUDENT),
            True, verbose)
