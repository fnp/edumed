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
        make_option('-a', '--attachments', dest='attachments', metavar="PATH", default='materialy',
            help='Attachments dir path.'),
        make_option('--ignore-incomplete', action='store_true', dest='ignore_incomplete', default=False,
            help='Attachments dir path.'),
    )
    help = 'Imports lessons from the specified directories.'
    args = 'directory [directory ...]'

    def import_book(self, file_path, options, attachments, ignore_incomplete=False):
        verbose = options.get('verbose')
        iofile = IOFile.from_filename(os.path.join(self.curdir, file_path))
        iofile.attachments = attachments
        return Lesson.publish(iofile, ignore_incomplete)

    @staticmethod
    def all_attachments(path):
        files = {}

        def read_dir(path):
            for name in os.listdir(path):
                fullname = os.path.join(path, name)
                if os.path.isdir(fullname):
                    read_dir(fullname)
                else:
                    f = IOFile.from_filename(fullname)
                    files[name] = f
                    files.setdefault(name.replace(" ", ""), f)

        read_dir(path)
        return files


    def handle(self, *directories, **options):
        from django.db import connection, transaction

        levels = set()
        self.style = color_style()
        
        verbose = options.get('verbose')
        self.curdir = os.path.abspath(os.curdir)


        # Start transaction management.
        # SQLite will choke on generating thumbnails 
        use_transaction = not connection.features.autocommits_when_autocommit_is_off
        if use_transaction:
            transaction.commit_unless_managed()
            transaction.enter_transaction_management()
            transaction.managed(True)
        else:
            print 'WARNING: Not using transaction management.'

        files_imported = 0
        files_skipped = 0

        for dir_name in directories:
            abs_dir = os.path.join(self.curdir, dir_name)
            if not os.path.isdir(abs_dir):
                print self.style.ERROR("%s: Not a directory. Skipping." % abs_dir)
            else:
                att_dir = os.path.join(abs_dir, options['attachments'])
                attachments = self.all_attachments(att_dir)

                # files queue
                files = sorted(os.listdir(abs_dir))
                postponed = {}
                ignore_incomplete = set()
                while files:
                    file_name = files.pop(0)
                    file_path = os.path.join(abs_dir, file_name)
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
                        lesson = self.import_book(file_path, options, attachments,
                                    ignore_incomplete=file_name in ignore_incomplete)
                    except Section.IncompleteError, e:
                        if file_name not in postponed or postponed[file_name] < files_imported:
                            # Push it back into the queue, maybe the missing lessons will show up.
                            if verbose > 0:
                                print self.style.NOTICE('Waiting for missing lessons.')
                            files.append(file_name)
                            postponed[file_name] = files_imported
                        elif options['ignore_incomplete'] and file_name not in ignore_incomplete:
                            files.append(file_name)
                            ignore_incomplete.add(file_name)
                            postponed[file_name] = files_imported
                        else:
                            # We're in a loop, nothing's being imported - some lesson is really missing.
                            raise e
                    except BaseException, e:
                        import traceback
                        traceback.print_exc()
                        files_skipped += 1
                    else:
                        files_imported += 1
                        if use_transaction:
                            transaction.commit()
                        if hasattr(lesson, 'level'):
                            levels.add(lesson.level)
                    finally:
                        if verbose > 0:
                            print


        if levels:
            print "Rebuilding level packages:"
            for level in levels:
                print level.name
                level.build_packages()

        # Print results
        print
        print "Results: %d files imported, %d skipped, %d total." % (
            files_imported, files_skipped, files_imported + files_skipped)
        print

        if use_transaction:
            transaction.commit()
            transaction.leave_transaction_management()
