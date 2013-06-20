from django import template
from django.utils.datastructures import SortedDict
from ..models import Competence, Curriculum, CurriculumCourse

register = template.Library()


@register.inclusion_tag("curriculum/snippets/competence.html")
def competence(texts, level):
    try:
        comps = [Competence.from_text(text) for text in texts]
    except:
        return {'texts': texts}
    return {
        'comps': comps,
        'level': level,
    }

@register.inclusion_tag("curriculum/snippets/curriculum.html")
def curriculum(identifiers):
    try:
        currs = [Curriculum.objects.get(identifier=identifier)
                    for identifier in identifiers]
    except Curriculum.DoesNotExist:
        return {'identifiers': identifiers}

    currset = SortedDict()
    for curr in currs:
        k = curr.course, curr.level
        if k not in currset:
            currset[k] = SortedDict()
        typename = Curriculum.TYPES[curr.type]
        if typename not in currset[k]:
            currset[k][typename] = []
        currset[k][typename].append(curr)

    return {
        'currset': currset,
    }
    

@register.filter
def url_for_level(comp, level):
    try:
        return comp.url_for_level(level)
    except:
        return comp.get_absolute_url()


@register.inclusion_tag("curriculum/snippets/course_box.html")
def course_box(course):
    lessons = SortedDict()
    for lesson in course.lesson_set.all():
        if lesson.level not in lessons:
            newdict = SortedDict()
            newdict['synthetic'] = []
            newdict['course'] = []
            lessons[lesson.level] = newdict
        if lesson.type not in lessons[lesson.level]:
            lessons[lesson.level][lesson.type] = []
        lessons[lesson.level][lesson.type].append(lesson)
    return {
        "course": course,
        "lessons": lessons,
    }

@register.inclusion_tag("curriculum/snippets/course_boxes.html")
def course_boxes():
    return {'object_list': CurriculumCourse.objects.all()}

@register.inclusion_tag("curriculum/snippets/course_boxes_toc.html")
def course_boxes_toc(accusative=False):
    return {
        'object_list': CurriculumCourse.objects.all(),
        'accusative': accusative,
    }
