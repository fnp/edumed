# -*- coding: utf-8 -*-
from urllib import unquote

from django.contrib.auth.decorators import permission_required
from django.http import Http404
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.cache import never_cache
from fnpdjango.utils.views import serve_file
from honeypot.decorators import check_honeypot

from .forms import contact_forms, update_forms
from .models import Attachment, Contact


@check_honeypot
@never_cache
def form(request, form_tag, force_enabled=False, contact_id=None, key=None):
    update = bool(contact_id and key)
    try:
        if update and form_tag in update_forms:
            form_class = update_forms[form_tag]
        else:
            form_class = contact_forms[form_tag]
    except KeyError:
        raise Http404
    if not (force_enabled and request.user.is_superuser):
        if form_class.is_disabled():
            template = getattr(form_class, 'disabled_template', None)
            if template:
                return render(request, template, {'title': form_class.form_title})
            raise Http404
    if contact_id:
        contact = get_object_or_404(Contact, id=contact_id, form_tag=form_tag)
        if form_tag != 'olimpiada':
            raise Http404
        confirmation = form_class.confirmation_class.objects.get(contact=contact)
        if key != confirmation.key:
            raise Http404
    else:
        contact = None
    if request.method == 'POST':
        form = form_class(request.POST, request.FILES, instance=contact)
    else:
        form = form_class(initial=request.GET, instance=contact)
    if request.method == 'POST':
        formsets = form.get_formsets(request)
        if form.is_valid() and all(formset.is_valid() for formset in formsets.itervalues()):
            form.save(request, formsets.values())
            return redirect('contact_thanks', form_tag)
    else:
        formsets = form.get_formsets()

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
