# -*- coding: utf-8 -*-
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from django.http import Http404
from django.http.response import HttpResponseRedirect, HttpResponse, HttpResponseForbidden
from django.shortcuts import get_object_or_404, render
from django.utils import timezone
from django.views.decorators.http import require_POST
from unidecode import unidecode

from stage2.forms import AttachmentForm, MarkForm
from stage2.models import Participant, Assignment, Answer, Attachment, Mark


def all_assignments(participant):
    assignments = Assignment.objects.all()
    for assignment in assignments:
        assignment.answer = assignment.answer_set.filter(participant=participant).first()
        assignment.forms = [
            (AttachmentForm(assignment=assignment, file_no=i, label=label, extensions=ext),
             assignment.answer.attachment_set.filter(file_no=i).first() if assignment.answer else None)
            for i, (label, ext) in enumerate(assignment.file_descriptions, 1)]
    return assignments


def participant_view(request, participant_id, key):
    participant = get_object_or_404(Participant, id=participant_id)
    if not participant.check(key):
        raise Http404
    return render(request, 'stage2/participant.html', {
        'participant': participant,
        'assignments': all_assignments(participant)})


@require_POST
def upload(request, assignment_id, participant_id, key):
    participant = get_object_or_404(Participant, id=participant_id)
    if not participant.check(key):
        raise Http404
    assignment = get_object_or_404(Assignment, id=assignment_id)
    now = timezone.now()
    if assignment.deadline < now:
        raise Http404  # TODO za późno
    for i, (label, ext) in enumerate(assignment.file_descriptions, 1):
        answer, created = Answer.objects.get_or_create(participant=participant, assignment=assignment)
        attachment, created = Attachment.objects.get_or_create(answer=answer, file_no=i)
        form = AttachmentForm(
            data=request.POST, files=request.FILES,
            assignment=assignment, file_no=i, label=label, instance=attachment, extensions=ext)
        if form.is_valid():
            form.save()
    return HttpResponseRedirect(reverse('stage2_participant', args=(participant_id, key)))


def attachment_download(attachment):
    response = HttpResponse(content_type='application/force-download')
    response.write(attachment.file.read())
    # workaround to this: https://code.djangoproject.com/ticket/20889
    response['Content-Disposition'] = 'attachment; filename="%s"' % unidecode(attachment.filename().replace('\n', ' '))
    response['Content-Length'] = response.tell()
    return response


def get_file(request, assignment_id, file_no, participant_id, key):
    """We want to serve submitted files back to participants, but also validate their keys,
       so static files are not good"""
    participant = get_object_or_404(Participant, id=participant_id)
    if not participant.check(key):
        raise Http404
    assignment = get_object_or_404(Assignment, id=assignment_id)
    answer = get_object_or_404(Answer, participant=participant, assignment=assignment)
    attachment = get_object_or_404(Attachment, answer=answer, file_no=file_no)
    return attachment_download(attachment)


@login_required
def assignment_list(request):
    assignments = request.user.stage2_assignments.all()
    if not assignments:
        return HttpResponseForbidden('Not allowed')
    for assignment in assignments:
        assignment.marked_count = Mark.objects.filter(expert=request.user, answer__assignment=assignment).count()
        assignment.to_mark_count = assignment.available_answers(request.user).count()
    non_empty_assignments = [ass for ass in assignments if ass.marked_count > 0 or ass.to_mark_count > 0]
    if len(non_empty_assignments) == 1 and non_empty_assignments[0].to_mark_count > 0:
        return HttpResponseRedirect(reverse('stage2_answer_list', args=[non_empty_assignments[0].id]))
    return render(request, 'stage2/assignment_list.html', {'assignments': assignments})


def available_answers(assignment, expert, answer_with_errors=None, form_with_errors=None, marked=False):
    if marked:
        answers = Answer.objects.filter(mark__expert=expert, assignment=assignment)
    else:
        answers = assignment.available_answers(expert)
    answers = answers.order_by('participant__last_name').prefetch_related('attachment_set')
    for answer in answers:
        attachments = answer.attachment_set.all()
        attachments_by_file_no = {attachment.file_no: attachment for attachment in attachments}
        answer.attachments = [
            (desc, attachments_by_file_no.get(i))
            for (i, (desc, ext)) in enumerate(assignment.file_descriptions, 1)]
        if answer == answer_with_errors:
            answer.form = form_with_errors
        else:
            answer.form = MarkForm(
                answer=answer, instance=answer.mark_set.filter(expert=expert).first(), prefix='ans%s' % answer.id)
    return answers


@login_required
def answer_list(request, assignment_id):
    assignment = get_object_or_404(Assignment, id=assignment_id)
    if request.user not in assignment.experts.all():
        return HttpResponseForbidden('Not allowed')
    return render(request, 'stage2/answer_list.html',
                  {'answers': available_answers(assignment, request.user), 'assignment': assignment})


@login_required
def marked_answer_list(request, assignment_id):
    assignment = get_object_or_404(Assignment, id=assignment_id)
    if request.user not in assignment.experts.all():
        return HttpResponseForbidden('Not allowed')
    return render(request, 'stage2/answer_list.html', {
        'answers': available_answers(assignment, request.user, marked=True),
        'assignment': assignment,
        'marked': True,
    })


@login_required
def expert_download(request, attachment_id):
    attachment = get_object_or_404(Attachment, id=attachment_id)
    return attachment_download(attachment)


@require_POST
@login_required
def mark_answer(request, answer_id):
    answer = get_object_or_404(Answer, id=answer_id)
    if request.user not in answer.assignment.experts.all():
        return HttpResponseForbidden('Not allowed')
    if answer.assignment.is_active():
        return HttpResponseForbidden('Not allowed')
    mark, created = Mark.objects.get_or_create(answer=answer, expert=request.user, defaults={'points': 0})
    form = MarkForm(data=request.POST, answer=answer, instance=mark, prefix='ans%s' % answer.id)
    if form.is_valid():
        form.save()
    elif created:
        mark.delete()

    return HttpResponseRedirect(reverse(
        'stage2_answer_list' if created else 'stage2_marked_answers', args=[answer.assignment_id]))
