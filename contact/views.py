# -*- coding: utf-8 -*-
from urllib import unquote

from datetime import datetime
from django.contrib.auth.decorators import permission_required
from django.http import Http404
from django.shortcuts import get_object_or_404, redirect, render
from django.utils import timezone
from django.views.decorators.cache import never_cache
from fnpdjango.utils.views import serve_file
from honeypot.decorators import check_honeypot

from edumed.utils import localtime_to_utc
from .forms import contact_forms
from .models import Attachment


@check_honeypot
@never_cache
def form(request, form_tag, force_enabled=False):
    try:
        form_class = contact_forms[form_tag]
    except KeyError:
        raise Http404
    if not (force_enabled and request.user.is_superuser):
        disabled = getattr(form_class, 'disabled', False)
        end_tuple = getattr(form_class, 'ends_on', None)
        end_time = localtime_to_utc(datetime(*end_tuple)) if end_tuple else None
        expired = end_time and end_time < timezone.now()
        if disabled or expired:
            template = getattr(form_class, 'disabled_template', None)
            if template:
                return render(request, template, {'title': form_class.form_title})
            raise Http404
    if request.method == 'POST':
        form = form_class(request.POST, request.FILES)
    else:
        form = form_class(initial=request.GET)
    formset_classes = getattr(form, 'form_formsets', {})
    if request.method == 'POST':
        formsets = {
            prefix: formset_class(request.POST, request.FILES, prefix=prefix)
            for prefix, formset_class in formset_classes.iteritems()}
        if form.is_valid() and all(formset.is_valid() for formset in formsets.itervalues()):
            form.save(request, formsets.values())
            return redirect('contact_thanks', form_tag)
    else:
        formsets = {prefix: formset_class(prefix=prefix) for prefix, formset_class in formset_classes.iteritems()}

    return render(
        request, ['contact/%s/form.html' % form_tag, 'contact/form.html'],
        {'form': form, 'formsets': formsets, 'formset_errors': any(formset.errors for formset in formsets.values())}
    )


def thanks(request, form_tag):
    try:
        form_class = contact_forms[form_tag]
    except KeyError:
        raise Http404

    return render(
        request, ['contact/%s/thanks.html' % form_tag, 'contact/thanks.html'],
        {'base_template': getattr(form_class, 'base_template', None)})


@permission_required('contact.change_attachment')
def attachment(request, contact_id, tag):
    attachment = get_object_or_404(Attachment, contact_id=contact_id, tag=tag)
    attachment_url = unquote(attachment.file.url)
    return serve_file(attachment_url)
