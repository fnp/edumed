# -*- coding: utf-8 -*-
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from django.http import Http404
from django.http.response import HttpResponseRedirect, HttpResponse, HttpResponseForbidden
from django.shortcuts import get_object_or_404, render
from django.utils import timezone
from django.utils.cache import patch_cache_control
from django.views.decorators.cache import never_cache
from django.views.decorators.http import require_POST
from unidecode import unidecode

from stage2.forms import AttachmentForm, MarkForm, AssignmentFieldForm
from stage2.models import Participant, Assignment, Answer, Attachment, Mark


def all_assignments(participant, sent_forms):
    assignments = Assignment.objects.all()
    if sent_forms:
        sent_assignment, field_forms, attachment_forms = sent_forms
    else:
        sent_assignment = field_forms = attachment_forms = None
    for assignment in assignments:
        assignment.answer, created = Answer.objects.get_or_create(participant=participant, assignment=assignment)
        if assignment == sent_assignment:
            assignment.field_forms = field_forms
            assignment.attachment_forms = attachment_forms
        else:
            assignment.field_forms = [
                AssignmentFieldForm(label=label, field_no=i, options=options, answer=assignment.answer)
                for i, (label, options) in enumerate(assignment.field_descriptions, 1)]
            assignment.attachment_forms = [
                (AttachmentForm(assignment=assignment, file_no=i, label=label, extensions=ext),
                 assignment.answer.attachment_set.filter(file_no=i).first() if assignment.answer else None)
                for i, (label, ext) in enumerate(assignment.file_descriptions, 1)]
    return assignments


@never_cache
def participant_view(request, participant_id, key):
    participant = get_object_or_404(Participant, id=participant_id)
    if not participant.check(key):
        raise Http404
    if request.POST:
        # ugly :/
        assignment_id = None
        for post_key, value in request.POST.iteritems():
            if post_key.endswith('assignment_id'):
                assignment_id = int(value)
        assert assignment_id

        assignment = get_object_or_404(Assignment, id=assignment_id)
        now = timezone.now()
        if assignment.deadline < now:
            raise Http404  # TODO za późno
        all_valid = True
        attachment_forms = []
        field_forms = []
        for i, (label, ext) in enumerate(assignment.file_descriptions, 1):
            answer, created = Answer.objects.get_or_create(participant=participant, assignment=assignment)
            attachment, created = Attachment.objects.get_or_create(answer=answer, file_no=i)
            form = AttachmentForm(
                data=request.POST, files=request.FILES,
                assignment=assignment, file_no=i, label=label, instance=attachment, extensions=ext)
            if form.is_valid():
                form.save()
            else:
                all_valid = False
            attachment_forms.append(form)
        for i, (label, options) in enumerate(assignment.field_descriptions, 1):
            answer = Answer.objects.get(participant=participant, assignment=assignment)
            form = AssignmentFieldForm(data=request.POST, label=label, field_no=i, options=options, answer=answer)
            if form.is_valid():
                form.save()
            else:
                all_valid = False
            field_forms.append(form)
        if all_valid:
            return HttpResponseRedirect(reverse('stage2_participant', args=(participant_id, key)))
        else:
            sent_forms = (assignment, field_forms, attachment_forms)
    else:
        sent_forms = None
    response = render(request, 'stage2/participant.html', {
        'participant': participant,
        'assignments': all_assignments(participant, sent_forms)})
    # not needed in Django 1.8
    patch_cache_control(response, no_cache=True, no_store=True, must_revalidate=True)
    return response


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
        assignment.supervisor = request.user in assignment.supervisors.all()
        assignment.arbiter_count = assignment.answer_set.filter(need_arbiter=True).count()

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


@login_required
def csv_results(request):
    import csv
    response = HttpResponse(content_type='text/csv')
    writer = csv.writer(response)
    assignments = Assignment.objects.all()
    participants = Participant.objects.filter(complete_set=True)
    headers = [u'imię', u'nazwisko', u'szkoła']
    assignments_experts = []
    for assignment in assignments:
        for expert in assignment.experts.filter(mark__answer__assignment=assignment).distinct():
            assignments_experts.append((assignment, expert))
            headers.append(u'%s %s' % (assignment.title, expert.last_name))
    for assignment in assignments:
        headers.append(u'%s - średnia' % assignment.title.encode('utf-8'))
    headers.append(u'ostateczny wynik')
    writer.writerow([unicode(item).encode('utf-8') for item in headers])
    for participant in participants:
        row = [
            participant.first_name,
            participant.last_name,
            participant.contact.body['school'],
        ]
        for assignment, expert in assignments_experts:
            try:
                row.append(
                    Mark.objects.get(
                        expert=expert, answer__assignment=assignment, answer__participant=participant).points)
            except Mark.DoesNotExist:
                row.append('')
        for assignment in assignments:
            row.append('%.2f' % participant.answer_set.get(assignment=assignment).score())
        row.append('%.2f' % participant.score())
        writer.writerow([unicode(item).encode('utf-8') for item in row])
    response['Content-Disposition'] = 'attachment; filename="wyniki.csv"'
    return response