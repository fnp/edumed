# -*- coding: utf-8 -*-
from django import forms
from django.utils.translation import ugettext_lazy as _
from pybb.forms import EditProfileForm
from pybb import util


class AvatarlessEditProfileForm(EditProfileForm):
    signature = forms.CharField(
        widget=forms.Textarea(attrs={'rows': 2, 'cols:': 60}),
        required=False,
        label=_('Signature')
    )

    class Meta:
        model = util.get_pybb_profile_model()
        fields = ['signature', 'time_zone', 'language', 'show_signatures']
