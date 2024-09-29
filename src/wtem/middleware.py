# -*- coding: utf-8 -*-
from threading import local


_thread_locals = local()


def get_current_request():
    return getattr(_thread_locals, 'request', None)


class ThreadLocalMiddleware(object):
    @staticmethod
    def process_request(request):
        _thread_locals.request = request
