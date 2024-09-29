# -*- coding: utf-8 -*-
from django.db import models

import pybb.models

from catalogue.models import Lesson


class Topic(models.Model):
    pybb_topic = models.OneToOneField(pybb.models.Topic, primary_key=True, related_name='edumed_topic')
    lesson = models.ForeignKey(Lesson, null=True, blank=True, related_name='forum_topics')
