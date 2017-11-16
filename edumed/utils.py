# -*- coding: utf-8 -*-
import codecs
import csv
import cStringIO

import pytz
from django.conf import settings
from django.utils import timezone

from settings.apps import INSTALLED_APPS


# source: https://docs.python.org/2/library/csv.html#examples
class UnicodeCSVWriter(object):
    """
    A CSV writer which will write rows to CSV file "f",
    which is encoded in the given encoding.
    """

    def __init__(self, f, dialect=csv.excel, encoding="utf-8", **kwds):
        # Redirect output to a queue
        self.queue = cStringIO.StringIO()
        self.writer = csv.writer(self.queue, dialect=dialect, **kwds)
        self.stream = f
        self.encoder = codecs.getincrementalencoder(encoding)()

    def writerow(self, row):
        self.writer.writerow([s.encode("utf-8") for s in row])
        # Fetch UTF-8 output from the queue ...
        data = self.queue.getvalue()
        data = data.decode("utf-8")
        # ... and reencode it into the target encoding
        data = self.encoder.encode(data)
        # write to the target stream
        self.stream.write(data)
        # empty queue
        self.queue.truncate(0)

    def writerows(self, rows):
        for row in rows:
            self.writerow(row)


def process_app_deps(list_with_deps):
    return tuple(
        (x[0] if type(x) == tuple else x)
        for x in list_with_deps
        if type(x) != tuple or x[1] in INSTALLED_APPS)


def localtime_to_utc(localtime):
    tz = pytz.timezone(settings.TIME_ZONE)
    return timezone.utc.normalize(
        tz.localize(localtime)
    )
