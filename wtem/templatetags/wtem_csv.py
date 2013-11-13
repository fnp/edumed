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
    toret = '%s' % submission.final_result
    examiners = submissionSet.examiners_by_exercise[exercise_id]
    marks_by_examiner = submission.get_exercise_marks_by_examiner(exercise_id)
    for examiner in examiners:
        mark = marks_by_examiner[examiner.id]
        toret += ','
        if mark is None:
            toret += '-'
        else:
            toret += str(mark)
    return toret
