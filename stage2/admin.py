# -*- coding: utf-8 -*-
from django.contrib import admin
from .models import Participant, Assignment, FieldOptionSet, FieldOption

admin.site.register(Assignment)
admin.site.register(Participant)
admin.site.register(FieldOptionSet)
admin.site.register(FieldOption)