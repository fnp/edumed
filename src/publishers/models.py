# -*- coding: utf-8 -*-
from django.db import models


class Publisher(models.Model):
    name = models.CharField(max_length=255)
    logo = models.ImageField(upload_to='publishers/logo')

    def __unicode__(self):
        return self.name
