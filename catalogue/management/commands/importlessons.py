# -*- coding: utf-8 -*-
# This file is part of EduMed, licensed under GNU Affero GPLv3 or later.
# Copyright © Fundacja Nowoczesna Polska. See NOTICE for more information.
#
import os
import sys
import time
from optparse import make_option
from django.conf import settings
from django.core.management.base import BaseCommand
from django.core.management.color import color_style
from django.core.files import File

from librarian import IOFile
from catalogue.models import Lesson, Section

#from search import Index


class Command(BaseCommand):
    option_list = BaseCommand.option_list + (
        make_option('-q', '--quiet', action='store_false', dest='verbose', default=True,
            help='Verbosity level; 0=minimal output, 1=normal output, 2=all output'),
    )
    help = 'Imports lessons from the specified directories.'
    args = 'directory [directory ...]'

    def import_book(self, file_path, options):
        verbose = options.get('verbose')
        iofile = IOFile.from_filename(file_path)
        basename, ext = file_path.rsplit('.', 1)
        if os.path.isdir(basename):
            for att_name in os.listdir(basename):
                iofile.attachments[att_name] = IOFile.from_filename(
                    os.path.join(basename, att_name))
        lesson = Lesson.publish(iofile)

    def handle(self, *directories, **options):
        from django.db import transaction

        self.style = color_style()
        
        verbose = options.get('verbose')

        # Start transaction management.
        transaction.commit_unless_managed()
        transaction.enter_transaction_management()
        transaction.managed(True)

        files_imported = 0
        files_skipped = 0

        for dir_name in directories:
            if not os.path.isdir(dir_name):
                print self.style.ERROR("%s: Not a directory. Skipping." % dir_name)
            else:
                # files queue
                files = sorted(os.listdir(dir_name))
                postponed = {}
                while files:
                    file_name = files.pop(0)
                    file_path = os.path.join(dir_name, file_name)
                    file_base, ext = os.path.splitext(file_path)

                    # Skip files that are not XML files
                    if not ext == '.xml':
                        continue

                    if verbose > 0:
                        print "Parsing '%s'" % file_path
                    else:
                        sys.stdout.write('.')
                        sys.stdout.flush()

                    # Import book files
                    try:
                        self.import_book(file_path, options)
                        files_imported += 1
                        transaction.commit()
                    except Section.IncompleteError, e:
                        if file_name not in postponed or postponed[file_name] < files_imported:
                            # Push it back into the queue, maybe the missing lessons will show up.
                            if verbose > 0:
                                print self.style.NOTICE('Waiting for missing lessons.')
                            files.append(file_name)
                            postponed[file_name] = files_imported
                        else:
                            # We're in a loop, nothing's being imported - some lesson is really missing.
                            raise e
                    except BaseException, e:
                        import traceback
                        traceback.print_exc()
                        files_skipped += 1

        # Print results
        print
        print "Results: %d files imported, %d skipped, %d total." % (
            files_imported, files_skipped, files_imported + files_skipped)
        print

        transaction.commit()
        transaction.leave_transaction_management()
