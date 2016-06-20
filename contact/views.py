# -*- coding: utf-8 -*-
from urllib import unquote

from django.contrib.auth.decorators import permission_required
from django.http import Http404
from django.shortcuts import get_object_or_404, redirect, render
from fnpdjango.utils.views import serve_file
from honeypot.decorators import check_honeypot

from .forms import contact_forms
from .models import Attachment


@check_honeypot
def form(request, form_tag, force_enabled=False):
    try:
        form_class = contact_forms[form_tag]
    except KeyError:
        raise Http404
    if (getattr(form_class, 'disabled', False) and
            not (force_enabled and request.user.is_superuser)):
        template = getattr(form_class, 'disabled_template', None)
        if template:
            return render(request, template, {'title': form_class.form_title})
        raise Http404
    if request.method == 'POST':
        form = form_class(request.POST, request.FILES)
        formsets = []
        valid = form.is_valid()
        for formset in getattr(form, 'form_formsets', ()):
            fset = formset(request.POST, request.FILES)
            if not fset.is_valid():
                valid = False
            formsets.append(fset)
        if valid:
            form.save(request, formsets)
            return redirect('contact_thanks', form_tag)
    else:
        form = form_class(initial=request.GET)
        formsets = []
        for formset in getattr(form, 'form_formsets', ()):
            formsets.append(formset())
    return render(
        request, ['contact/%s/form.html' % form_tag, 'contact/form.html'],
        {'form': form, 'formsets': formsets}
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
