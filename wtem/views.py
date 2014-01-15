import os

from django.shortcuts import render
from django.utils import simplejson
from django.conf import settings
from django.http import Http404, HttpResponseForbidden
from django.views.decorators.csrf import csrf_exempt

from .models import Submission, DEBUG_KEY, exercises
from .forms import WTEMForm

WTEM_CONTEST_STAGE = getattr(settings, 'WTEM_CONTEST_STAGE', 'before')


@csrf_exempt
def form(request, key):
    return globals()['form_' + WTEM_CONTEST_STAGE](request, key)
    
def form_before(request, key):
    try:
        submission = Submission.objects.get(key = key)
    except:
        return render(request, 'wtem/key_not_found_before.html')
    else:
        return render(request, 'wtem/main_before.html')

def form_after(request, key):
    return render(request, 'wtem/main_after.html')

@csrf_exempt
def form_during(request, key):

    if WTEM_CONTEST_STAGE != 'during':
        if request.META['REMOTE_ADDR'] != getattr(settings, 'WTEM_CONTEST_IP_ALLOW', 'xxx'):
            return HttpResponseForbidden('Not allowed')

    try:
        submission = Submission.objects.get(key = key)
    except Submission.DoesNotExist:
        if settings.DEBUG and key == DEBUG_KEY:
            submission = Submission.create(first_name = 'Debug', last_name = 'Debug', email = 'debug@debug.com', key = DEBUG_KEY)
        else:
            return render(request, 'wtem/key_not_found.html')
    if request.method == 'GET':
        return render(request, 'wtem/main.html', dict(exercises = exercises, end_time = submission.end_time))
    elif request.method == 'POST':
        form = WTEMForm(request.POST, request.FILES, instance = submission)
        if form.is_valid():
            form.save()
            return render(request, 'wtem/thanks.html', dict(end_time = submission.end_time))
        else:
            raise Exception
