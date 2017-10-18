# -*- coding: utf-8 -*-
import json
from copy import deepcopy

from django.conf import settings
from django.core.urlresolvers import reverse
from django.http import HttpResponseForbidden
from django.http.response import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.views.decorators.cache import never_cache
from django.views.decorators.csrf import csrf_exempt

from wtem.models import Confirmation
from .forms import WTEMForm, WTEMSingleForm
from .models import Submission, DEBUG_KEY, exercises, CompetitionState

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
    exercises_with_answers = deepcopy(exercises)
    if submission.answers:
        answers = json.loads(submission.answers)
    else:
        answers = {}
    for exercise in exercises_with_answers:
        exercise['saved_answer'] = answers.get(str(exercise['id']), '')
        if exercise['type'] == 'open' and exercise.get('fields'):
            field_answers = {field['id']: field['text'] for field in exercise['saved_answer']}
            for field in exercise['fields']:
                field['saved_answer'] = field_answers.get(field['id'], '')
    if request.method == 'GET':
        return render(request, 'wtem/main.html', {'exercises': exercises_with_answers, 'end_time': submission.end_time})
    elif request.method == 'POST':
        form = WTEMForm(request.POST, request.FILES, instance=submission)
        if form.is_valid():
            form.save()
            return render(request, 'wtem/thanks.html', dict(end_time=submission.end_time))
        else:
            raise Exception


@never_cache
@csrf_exempt
def form_single(request, submission_id, key):
    if CompetitionState.get_state() != CompetitionState.DURING:
        if request.META['REMOTE_ADDR'] not in getattr(settings, 'WTEM_CONTEST_IP_ALLOW', []):
            return HttpResponseForbidden('Not allowed')

    submission = Submission.objects.get(id=submission_id)
    if submission.key != key:
        return render(request, 'wtem/key_not_found.html')

    i, exercise = submission.current_exercise()

    if not exercise:
        return render(request, 'wtem/thanks_single.html')

    if request.method == 'GET':
        return render(request, 'wtem/single.html', {'exercise': exercise, 'no': i})
    elif request.method == 'POST':
        form = WTEMSingleForm(request.POST, request.FILES, instance=submission)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('form_single', kwargs={'submission_id': submission_id, 'key': key}))
        else:
            raise Exception


def confirmation(request, id, key):
    conf = get_object_or_404(Confirmation, id=id, key=key)
    was_confirmed = conf.confirmed
    if not was_confirmed:
        conf.confirmed = True
        conf.save()
    return render(request, 'wtem/confirmed.html', {'confirmation': conf, 'was_confirmed': was_confirmed})
