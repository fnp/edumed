# -*- coding: utf-8 -*-
# This file is part of EduMed, licensed under GNU Affero GPLv3 or later.
# Copyright © Fundacja Nowoczesna Polska. See NOTICE for more information.
#
import os
import sys
from optparse import make_option

from django.core.management.base import BaseCommand
from django.db import transaction

from catalogue.models import Lesson, Section
from librarian import IOFile


class Command(BaseCommand):
    option_list = BaseCommand.option_list + (
        make_option('-q', '--quiet', action='store_false', dest='verbose', default=True,
                    help='Verbosity level; 0=minimal output, 1=normal output, 2=all output'),
        make_option('-a', '--attachments', dest='attachments', metavar="PATH", default='materialy',
                    help='Attachments dir path.'),
        make_option('--ignore-incomplete', action='store_true', dest='ignore_incomplete', default=False,
                    help='Attachments dir path.'),
        make_option('--dont-repackage', action='store_false', dest='repackage', default=True,
                    help='Don\'t refresh level packages.'),
    )
    help = 'Imports lessons from the specified directories.'
    args = 'directory [directory ...]'

    def __init__(self):
        super(Command, self).__init__()
        self.options = None
        self.levels = None

    @staticmethod
    def all_attachments(path):
        files = {}
        if not os.path.isdir(path):
            return files

        def read_dir(path):
            for name in os.listdir(path):
                fullname = os.path.join(path, name)
                if os.path.isdir(fullname):
                    read_dir(fullname)
                else:
                    f = IOFile.from_filename(fullname)
                    files[name.decode('utf-8')] = f
                    files.setdefault(name.replace(" ", "").decode('utf-8'), f)

        read_dir(path)
        return files

    @transaction.atomic
    def handle(self, *directories, **options):

        repackage = options.get('repackage')

        self.levels = set()

        curdir = os.path.abspath(os.curdir)
        self.options = options

        files_imported = 0
        files_skipped = 0

        for dir_name in directories:
            abs_dir = os.path.join(curdir, dir_name)
            if not os.path.isdir(abs_dir):
                print self.style.ERROR("%s: Not a directory. Skipping." % abs_dir)
            else:
                files_imported_dir, files_skipped_dir = self.import_from_dir(abs_dir)
                files_imported += files_imported_dir
                files_skipped += files_skipped_dir

        if self.levels and repackage:
            print "Rebuilding level packages:"
            for level in self.levels:
                print level.name
                level.build_packages()

        # Print results
        print
        print "Results: %d files imported, %d skipped, %d total." % (
            files_imported, files_skipped, files_imported + files_skipped)
        print

    def import_from_dir(self, abs_dir):
        verbose = self.options.get('verbose')
        files_imported = 0
        files_skipped = 0
        att_dir = os.path.join(abs_dir, self.options['attachments'])
        attachments = self.all_attachments(att_dir)
        # files queue
        files = sorted(os.listdir(abs_dir))
        postponed = {}
        ignore_incomplete = set()
        while files:
            file_name = files.pop(0)
            file_path = os.path.join(abs_dir, file_name)
            file_base, ext = os.path.splitext(file_path)

            if os.path.isdir(file_path):
                dir_imported, dir_skipped = self.import_from_dir(file_path)
                files_imported += dir_imported
                files_skipped += files_skipped
                continue

            # Skip files that are not XML files
            if not ext == '.xml':
                continue

            if verbose > 0:
                print "Parsing '%s'" % file_path
            else:
                sys.stdout.write('.')
                sys.stdout.flush()

            try:
                iofile = IOFile.from_filename(file_path)
                iofile.attachments = attachments
                lesson = Lesson.publish(iofile, file_name in ignore_incomplete)
            except Section.IncompleteError:
                if file_name not in postponed or postponed[file_name] < files_imported:
                    # Push it back into the queue, maybe the missing lessons will show up.
                    if verbose > 0:
                        print self.style.NOTICE('Waiting for missing lessons.')
                    files.append(file_name)
                    postponed[file_name] = files_imported
                elif self.options['ignore_incomplete'] and file_name not in ignore_incomplete:
                    files.append(file_name)
                    ignore_incomplete.add(file_name)
                    postponed[file_name] = files_imported
                else:
                    # We're in a loop, nothing's being imported - some lesson is really missing.
                    raise
            except BaseException:
                import traceback
                traceback.print_exc()
                files_skipped += 1
            else:
                files_imported += 1
                if hasattr(lesson, 'level'):
                    self.levels.add(lesson.level)
            finally:
                if verbose > 0:
                    print
        return files_imported, files_skipped
