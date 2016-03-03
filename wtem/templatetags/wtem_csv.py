# -*- coding: utf-8 -*-
from django import template

register = template.Library()


@register.simple_tag
def csv_header(exercise_id, submissionSet):
    examiners = submissionSet.examiners_by_exercise.get(exercise_id, [])
    examiners_string = ','.join(['zad %s - %s' % (exercise_id, user.username) for user in examiners])
    toret = ',zad %s' % exercise_id
    if examiners_string:
        toret += ',' + examiners_string
    return toret


@register.simple_tag
def csv_row_fragment(exercise_id, submission, submissionSet):
    final_mark = submission.get_final_exercise_mark(exercise_id)
    if final_mark is not None:
        final_mark = ('%.2f' % final_mark).rstrip('0').rstrip('.')
    toret = final_mark if final_mark else '-'
    examiners = submissionSet.examiners_by_exercise.get(exercise_id, [])
    marks_by_examiner = submission.get_exercise_marks_by_examiner(exercise_id)
    for examiner in examiners:
        mark = marks_by_examiner.get(str(examiner.id), None)
        toret += ','
        if mark is None:
            toret += '"-"'
        else:
            toret += str(mark)
    return toret
