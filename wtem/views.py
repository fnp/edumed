# -*- coding: utf-8 -*-

from django.conf import settings
from django.http import HttpResponseForbidden
from django.shortcuts import render
from django.views.decorators.cache import never_cache
from django.views.decorators.csrf import csrf_exempt

from .forms import WTEMForm
from .models import Submission, DEBUG_KEY, exercises

WTEM_CONTEST_STAGE = getattr(settings, 'WTEM_CONTEST_STAGE', 'before')


@csrf_exempt
def form(request, key):
    return globals()['form_' + WTEM_CONTEST_STAGE](request, key)


def form_before(request, key):
    try:
        Submission.objects.get(key=key)
    except Submission.DoesNotExist:
        return render(request, 'wtem/key_not_found_before.html')
    else:
        return render(request, 'wtem/main_before.html')


def form_after(request, key):
    return render(request, 'wtem/main_after.html')


@never_cache
@csrf_exempt
def form_during(request, key):

    if WTEM_CONTEST_STAGE != 'during':
        if request.META['REMOTE_ADDR'] not in getattr(settings, 'WTEM_CONTEST_IP_ALLOW', []):
            return HttpResponseForbidden('Not allowed')

    try:
        submission = Submission.objects.get(key=key)
    except Submission.DoesNotExist:
        if settings.DEBUG and key == DEBUG_KEY:
            submission = Submission.create(
                first_name='Debug', last_name='Debug', email='debug@debug.com', key=DEBUG_KEY)
        else:
            return render(request, 'wtem/key_not_found.html')
    if request.method == 'GET':
        return render(request, 'wtem/main.html', dict(exercises=exercises, end_time=submission.end_time))
    elif request.method == 'POST':
        form = WTEMForm(request.POST, request.FILES, instance=submission)
        if form.is_valid():
            form.save()
            return render(request, 'wtem/thanks.html', dict(end_time=submission.end_time))
        else:
            raise Exception
