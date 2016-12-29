# -*- coding: utf-8 -*-
from django.core.urlresolvers import reverse
from django.http import Http404
from django.http.response import HttpResponseRedirect, HttpResponse
from django.shortcuts import get_object_or_404, render
from django.utils import timezone
from django.views.decorators.http import require_POST

from stage2.forms import AttachmentForm
from stage2.models import Participant, Assignment, Answer, Attachment


def participant_view(request, participant_id, key):
    participant = get_object_or_404(Participant, id=participant_id)
    if not participant.check(key):
        raise Http404
    now = timezone.now()
    assignments = Assignment.objects.all()
    for assignment in assignments:
        assignment.active = assignment.deadline >= now
        assignment.answer = assignment.answer_set.filter(participant=participant).first()
        assignment.forms = [
            (AttachmentForm(assignment=assignment, file_no=i, label=label),
             assignment.answer.attachment_set.filter(file_no=i).first() if assignment.answer else None)
            for i, label in enumerate(assignment.file_descriptions, 1)]
    return render(request, 'stage2/participant.html', {
        'participant': participant,
        'assignments': assignments})


@require_POST
def upload(request, assignment_id, participant_id, key):
    participant = get_object_or_404(Participant, id=participant_id)
    if not participant.check(key):
        raise Http404
    assignment = get_object_or_404(Assignment, id=assignment_id)
    now = timezone.now()
    if assignment.deadline < now:
        raise Http404  # TODO za późno
    for i, label in enumerate(assignment.file_descriptions, 1):
        answer, created = Answer.objects.get_or_create(participant=participant, assignment=assignment)
        attachment, created = Attachment.objects.get_or_create(answer=answer, file_no=i)
        form = AttachmentForm(
            data=request.POST, files=request.FILES,
            assignment=assignment, file_no=i, label=label, instance=attachment)
        if form.is_valid():
            form.save()
    return HttpResponseRedirect(reverse('stage2_participant', args=(participant_id, key)))


def get_file(request, assignment_id, file_no, participant_id, key):
    """We want to serve submitted files back to participants, but also validate their keys,
       so static files are not good"""
    participant = get_object_or_404(Participant, id=participant_id)
    if not participant.check(key):
        raise Http404
    assignment = get_object_or_404(Assignment, id=assignment_id)
    answer = get_object_or_404(Answer, participant=participant, assignment=assignment)
    attachment = get_object_or_404(Attachment, answer=answer, file_no=file_no)
    response = HttpResponse(content_type='application/force-download')
    response.write(attachment.file.read())
    response['Content-Disposition'] = 'attachment; filename="%s"' % attachment.filename()
    response['Content-Length'] = response.tell()
    return response
