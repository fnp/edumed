# -*- coding: utf-8 -*-
from django import forms
from django.forms.util import flatatt
from django.utils.html import format_html


class HeaderWidget(forms.widgets.Widget):
    def render(self, name, value, attrs=None):
        attrs.update(self.attrs)
        return format_html('<a{0}></a>', flatatt(attrs))
