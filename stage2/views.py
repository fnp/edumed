# -*- coding: utf-8 -*-
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from django.http import Http404
from django.http.response import HttpResponseRedirect, HttpResponse, HttpResponseForbidden
from django.shortcuts import get_object_or_404, render
from django.utils import timezone
from django.utils.cache import patch_cache_control
from django.views.decorators.cache import never_cache
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
            return HttpResponseForbidden('Not Allowed')
        attachments_valid, attachment_forms = get_attachment_forms(assignment, participant, request)
        fields_valid, field_forms = get_field_forms(assignment, participant, request)
        if attachments_valid and fields_valid:
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


def get_attachment_forms(assignment, participant, request):
    all_valid = True
    attachment_forms = []
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
    return all_valid, attachment_forms


def get_field_forms(assignment, participant, request):
    all_valid = True
    field_forms = []
    for i, (label, options) in enumerate(assignment.field_descriptions, 1):
        answer = Answer.objects.get(participant=participant, assignment=assignment)
        form = AssignmentFieldForm(data=request.POST, label=label, field_no=i, options=options, answer=answer)
        if form.is_valid():
            form.save()
        else:
            all_valid = False
        field_forms.append(form)
    return all_valid, field_forms


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
    expert = request.user
    assignments = expert.stage2_assignments.all()
    if not assignments:
        return HttpResponseForbidden('Not allowed')
    for assignment in assignments:
        assignment.marked_count = assignment.available_answers(expert, marked=True).count()
        assignment.to_mark_count = assignment.available_answers(expert).count()
        assignment.supervisor = expert in assignment.supervisors.all()
        assignment.arbiter_count = assignment.needing_arbiter().count()

    non_empty_assignments = [ass for ass in assignments if ass.marked_count > 0 or ass.to_mark_count > 0]
    if len(non_empty_assignments) == 1 and non_empty_assignments[0].to_mark_count > 0:
        return HttpResponseRedirect(reverse('stage2_answer_list', args=[non_empty_assignments[0].id]))
    return render(request, 'stage2/assignment_list.html', {'assignments': assignments})


def available_answers(assignment, expert, sent_forms=None, marked=False):
    if marked:
        answers = assignment.available_answers(expert, marked=True)
    else:
        answers = assignment.available_answers(expert).order_by('participant__last_name')
    answers = answers.prefetch_related('attachment_set')
    if sent_forms:
        sent_answer_id, mark_forms = sent_forms
    else:
        sent_answer_id = mark_forms = None
    for answer in answers:
        attachments = answer.attachment_set.all()
        attachments_by_file_no = {attachment.file_no: attachment for attachment in attachments}
        answer.attachments = [
            (desc, attachments_by_file_no.get(i))
            for (i, (desc, ext)) in enumerate(assignment.file_descriptions, 1)]
        if answer.id == sent_answer_id:
            answer.forms = mark_forms
        else:
            answer.forms = []
            for criterion in assignment.markcriterion_set.all():
                answer.forms.append(MarkForm(
                    answer=answer,
                    criterion=criterion,
                    instance=answer.mark_set.filter(expert=expert, criterion=criterion).first(),
                    prefix='mark%s-%s' % (answer.id, criterion.id)))
    return answers


@login_required
def answer_list(request, assignment_id, marked=False):
    assignment = get_object_or_404(Assignment, id=assignment_id)
    expert = request.user
    if expert not in assignment.experts.all():
        return HttpResponseForbidden('Not allowed')
    if request.POST:
        # ugly :/
        answer_id = None
        for post_key, value in request.POST.iteritems():
            if post_key.endswith('answer_id'):
                answer_id = int(value)
        answer = get_object_or_404(Answer, id=answer_id)

        if answer not in assignment.available_answers(expert, marked=marked):
            return HttpResponseForbidden('Not allowed')
        if answer.assignment.is_active():
            return HttpResponseForbidden('Not allowed')
        all_valid, forms = get_mark_forms(answer, request)
        if all_valid:
            if marked:
                return HttpResponseRedirect(reverse('stage2_marked_answers', args=[answer.assignment_id]))
            else:
                return HttpResponseRedirect(reverse('stage2_answer_list', args=[answer.assignment_id]))
        else:
            sent_forms = answer_id, forms
    else:
        sent_forms = None
    answers = available_answers(assignment, expert, sent_forms=sent_forms, marked=marked)
    return render(request, 'stage2/answer_list.html', {
        'answers': answers,
        'assignment': assignment,
        'field_counts': assignment.field_counts(answers) if not marked else None,
        'supervisor': expert in assignment.supervisors.all(),
        'marked': marked
    })


def get_mark_forms(answer, request):
    all_valid = True
    created_marks = []
    forms = []
    for criterion in answer.assignment.markcriterion_set.all():
        mark, created = Mark.objects.get_or_create(
            answer=answer, criterion=criterion, expert=request.user, defaults={'points': 0})
        if created:
            created_marks.append(mark)
        form = MarkForm(
            data=request.POST, answer=answer, criterion=criterion, instance=mark,
            prefix='mark%s-%s' % (answer.id, criterion.id))
        if form.is_valid():
            form.save()
        else:
            all_valid = False
        forms.append(form)
    if not all_valid:
        for mark in created_marks:
            mark.delete()
    return all_valid, forms


@login_required
def expert_download(request, attachment_id):
    attachment = get_object_or_404(Attachment, id=attachment_id)
    return attachment_download(attachment)


@login_required
def csv_results(request):
    import csv
    response = HttpResponse(content_type='text/csv')
    writer = csv.writer(response)
    assignments = Assignment.objects.all()
    participants = Participant.objects.filter(complete_set=True)
    headers = [u'imię', u'nazwisko', u'szkoła', u'adres szkoły']
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
            participant.contact.body['school_address'],
        ]
        for assignment, expert in assignments_experts:
            marks = expert.mark_set.filter(answer__assignment=assignment, answer__participant=participant)
            if marks:
                row.append(sum(mark.points for mark in marks))
            else:
                row.append('')
        for assignment in assignments:
            row.append('%.2f' % participant.answer_set.get(assignment=assignment).score())
        row.append('%.2f' % participant.score())
        writer.writerow([unicode(item).encode('utf-8') for item in row])
    response['Content-Disposition'] = 'attachment; filename="wyniki.csv"'
    return response
