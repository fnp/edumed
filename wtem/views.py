import os

from django.shortcuts import render
from django.utils import simplejson


def main(request):
    ## @@ move this out of the view
    f = file(os.path.dirname(__file__) + '/fixtures/exercises.json')
    exercises = simplejson.loads(f.read())
    f.close()

    return render(request, 'wtem/main.html', dict(exercises = exercises))
