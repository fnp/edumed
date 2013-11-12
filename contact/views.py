from django.contrib.auth.decorators import permission_required
from django.http import Http404, HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.utils.translation import ugettext_lazy as _
from fnpdjango.utils.views import serve_file
from .forms import contact_forms
from .models import Attachment


def form(request, form_tag):
    try:
        form_class = contact_forms[form_tag]
    except KeyError:
        raise Http404
    if getattr(form_class, 'disabled', False):
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
    return render(request,
                ['contact/%s/form.html' % form_tag, 'contact/form.html'],
                {'form': form, 'formsets': formsets}
            )


def thanks(request, form_tag):
    try:
        form_class = contact_forms[form_tag]
    except KeyError:
        raise Http404

    return render(request,
                ['contact/%s/thanks.html' % form_tag, 'contact/thanks.html'],
                dict(base_template = getattr(form_class, 'base_template', None))
            )


@permission_required('contact.change_attachment')
def attachment(request, contact_id, tag):
    attachment = get_object_or_404(Attachment, contact_id=contact_id, tag=tag)
    return serve_file(attachment.file.url)
