# -*- coding: utf-8 -*-
from django.contrib import admin
from .models import Participant, Assignment


admin.site.register(Assignment)
admin.site.register(Participant)
