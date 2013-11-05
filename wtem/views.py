import os

from django.shortcuts import render
from django.utils import simplejson
from django.conf import settings
from django.http import Http404

from .models import Submission, DEBUG_KEY
from .forms import WTEMForm

WTEM_CONTEST_STAGE = getattr(settings, 'WTEM_CONTEST_STAGE', 'before')


def main(request):
    pass

def form(request, key):
    return globals()['form_' + WTEM_CONTEST_STAGE](request, key)
    
def form_before(request, key):
    return render(request, 'wtem/main_before.html')

def form_after(request, key):
    return render(request, 'wtem/main_after.html')

def form_during(request, key):

    if WTEM_CONTEST_STAGE != 'during':
        if request.META['REMOTE_ADDR'] != getattr(settings, 'WTEM_CONTEST_IP_ALLOW', 'xxx'):
            raise Http404

    try:
        submission = Submission.objects.get(key = key)
    except Submission.DoesNotExist:
        if settings.DEBUG and key == DEBUG_KEY:
            submission = Submission.create(first_name = 'Debug', last_name = 'Debug', email = 'debug@debug.com', key = DEBUG_KEY)
        else:
            raise Http404

    ## @@ move this out of the view
    f = file(os.path.dirname(__file__) + '/fixtures/exercises.json')
    exercises = simplejson.loads(f.read())
    f.close()

    if request.method == 'GET':
        return render(request, 'wtem/main.html', dict(exercises = exercises))
    elif request.method == 'POST':
        form = WTEMForm(request.POST, request.FILES, instance = submission)
        if form.is_valid():
            form.save()
            return render(request, 'wtem/thanks.html')
        else:
            raise Exception