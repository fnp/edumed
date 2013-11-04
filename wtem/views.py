import os

from django.shortcuts import render
from django.utils import simplejson
from django.conf import settings
from django.http import Http404

from .models import Submission
from .forms import WTEMForm


def main(request):
    pass

def form(request, key):
    try:
        submission = Submission.objects.get(key = key)
    except Submission.DoesNotExist:
        if settings.DEBUG and key == '12345':
            submission = Submission.create(first_name = 'Debug', last_name = 'Debug', email = 'debug@debug.com', key = '12345')[0]
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
