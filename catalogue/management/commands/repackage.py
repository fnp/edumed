# -*- coding: utf-8 -*-
# This file is part of EduMed, licensed under GNU Affero GPLv3 or later.
# Copyright © Fundacja Nowoczesna Polska. See NOTICE for more information.
#
from optparse import make_option
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = 'Rebuilds downloadable packages.'

    def handle(self, **options):
        from curriculum.models import Level

        for level in Level.objects.all():
            level.build_packages()
