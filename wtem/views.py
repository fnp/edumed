# -*- coding: utf-8 -*-
import json
from copy import deepcopy
from functools import wraps

from django.conf import settings
from django.contrib import messages
from django.core.urlresolvers import reverse
from django.http import HttpResponseForbidden
from django.http.response import HttpResponseRedirect, Http404
from django.shortcuts import render, get_object_or_404
from django.utils import timezone
from django.utils.cache import patch_cache_control, add_never_cache_headers
from django.views.decorators.cache import never_cache
from django.views.decorators.csrf import csrf_exempt

from wtem.models import Confirmation, TeacherConfirmation
from .forms import WTEMForm, WTEMSingleForm
from .models import Submission, DEBUG_KEY, exercises, CompetitionState


def cache_until_start(view_func):
    @wraps(view_func)
    def _wrapped_view_func(request, *args, **kwargs):
        response = view_func(request, *args, **kwargs)
        max_age = max(int((CompetitionState.start - timezone.now()).total_seconds()) + 1, 0)
        if max_age:
            patch_cache_control(response, max_age=max_age)
        else:
            add_never_cache_headers(response)
        return response

    return _wrapped_view_func


def get_submission(submission_id):
    try:
        submission_id = int(submission_id)
    except ValueError:
        raise Http404
    return get_object_or_404(Submission, id=submission_id)


@csrf_exempt
def form(request, submission_id, key):
    state = CompetitionState.get_state()
    if state == CompetitionState.DURING:
        state = 'single'
    if request.META['REMOTE_ADDR'] in getattr(settings, 'WTEM_CONTEST_IP_ALLOW', []):
        state = 'single'
    return globals()['form_' + state](request, submission_id, key)


@cache_until_start
def form_before(request, submission_id, key):
    submission = get_submission(submission_id)
    if submission.key != key:
        return render(request, 'wtem/key_not_found_before.html')
    else:
        submission.opened_link = True
        submission.save()
        return render(request, 'wtem/main_before.html')


def form_after(request, submission_id, key):
    return render(request, 'wtem/main_after.html')


@never_cache
@csrf_exempt
def form_during(request, key):

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
        return render(request, 'wtem/main.html', {
            'exercises': exercises_with_answers,
            'end_time': submission.end_time,
            'show_answers': True,
        })
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

    submission = get_submission(submission_id)
    if submission.key != key:
        return render(request, 'wtem/key_not_found.html')

    i, exercise = submission.current_exercise()

    exercise_count = len(exercises)

    if not exercise:
        return render(request, 'wtem/thanks_single.html')

    if request.method == 'GET':
        return render(request, 'wtem/single.html', {'exercise': exercise, 'no': i, 'exercise_count': exercise_count})
    elif request.method == 'POST':
        form = WTEMSingleForm(request.POST, request.FILES, instance=submission)
        if form.is_valid():
            try:
                form.save()
            except ValueError as e:
                if e.message == 'wrong exercise id':
                    messages.error(request, u'Próba wysłania odpowiedzi ponownie lub poza kolejnością')
                elif e.message == 'no answer':
                    messages.error(request, u'Wybierz przynajmniej jedną odpowiedź')
            return HttpResponseRedirect(reverse('wtem_form', kwargs={'submission_id': submission_id, 'key': key}))
        else:
            raise Exception(u'Błędna wartość w formularzu')


@cache_until_start
@csrf_exempt
def start(request, submission_id, key):
    state = CompetitionState.get_state()
    if state in (CompetitionState.BEFORE, CompetitionState.AFTER):
        return globals()['form_' + state](request, submission_id, key)

    submission = get_submission(submission_id)
    if submission.key != key:
        return render(request, 'wtem/key_not_found.html')

    submission.opened_link = True
    submission.save()

    i, exercise = submission.current_exercise()
    if not exercise:
        return render(request, 'wtem/thanks_single.html')

    return render(request, 'wtem/start.html', {'exercise_count': len(exercises), 'submission': submission})


def confirmation(request, id, key):
    conf = get_object_or_404(Confirmation, id=id, key=key)
    was_confirmed = conf.confirmed
    if not was_confirmed:
        conf.confirmed = True
        conf.save()
    return render(request, 'wtem/confirmed.html', {'confirmation': conf, 'was_confirmed': was_confirmed})


def teacher_confirmation(request, id, key):
    conf = get_object_or_404(TeacherConfirmation, id=id, key=key)
    was_confirmed = conf.confirmed
    if not was_confirmed:
        conf.confirmed = True
        conf.save()
    from contact.forms import contact_forms
    form_class = contact_forms['olimpiada']
    if not form_class.is_disabled():
        pass
    return render(request, 'wtem/teacher_confirmed.html', {
        'confirmation': conf,
        'was_confirmed': was_confirmed,
    })
