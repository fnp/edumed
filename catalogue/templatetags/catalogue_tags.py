from collections import defaultdict
from django import template
from django.utils.datastructures import SortedDict
from ..models import Lesson, Section
from curriculum.models import Level, CurriculumCourse
from librarian.dcparser import WLURI, Person

register = template.Library()


@register.inclusion_tag("catalogue/snippets/carousel.html")
def catalogue_carousel():
    return {
        "object_list": Section.objects.all()
    }

@register.inclusion_tag("catalogue/snippets/levels_main.html")
def catalogue_levels_main():
    object_list = Level.objects.exclude(lesson=None)
    c = object_list.count()
    return {
        'object_list': object_list,
        'section_width': (700 - 20 * (c - 1)) / c,
    }


@register.inclusion_tag("catalogue/snippets/level_box.html")
def level_box(level):
    lessons = dict(
        synthetic = [],
        course = SortedDict(),
        project = [],
    )
    by_course = defaultdict(lambda: defaultdict(list))

    lesson_lists = [alist for alist in [
        list(level.lesson_set.exclude(type='appendix').order_by('section__order')),
        list(level.lessonstub_set.all())
    ] if alist]

    while lesson_lists:
        min_index, min_list = min(enumerate(lesson_lists), key=lambda x: x[1][0].order)
        lesson = min_list.pop(0)
        if not min_list:
            lesson_lists.pop(min_index)

        if lesson.type == 'course':
            if lesson.section not in lessons['course']:
                lessons['course'][lesson.section] = []
            lessons['course'][lesson.section].append(lesson)
        else:
            lessons[lesson.type].append(lesson)

        if hasattr(lesson, 'curriculum_courses'):
            for course in lesson.curriculum_courses.all():
                by_course[course][lesson.type].append(lesson)

    courses = [(course, by_course[course]) for course in
        CurriculumCourse.objects.filter(lesson__level=level).distinct()]

    return {
        "level": level,
        "lessons": lessons,
        "courses": courses,
    }

@register.inclusion_tag("catalogue/snippets/lesson_nav.html")
def lesson_nav(lesson):
    if lesson.type == 'course':
        root = lesson.section
        siblings = Lesson.objects.filter(type='course', level=lesson.level, section=root)
    elif lesson.type == 'appendix':
        root = None
        siblings = Lesson.objects.filter(type=lesson.type)
    else:
        root = None
        siblings = Lesson.objects.filter(type=lesson.type, level=lesson.level)
    return {
        "lesson": lesson,
        "root": root,
        "siblings": siblings,
    }

@register.inclusion_tag("catalogue/snippets/lesson_link.html")
def lesson_link(uri):
    try:
        return {'lesson': Lesson.objects.get(slug=WLURI(uri).slug)}
    except Lesson.DoesNotExist:
        return {}

@register.filter
def person_list(persons):
    return u", ".join(Person.from_text(p).readable() for p in persons)


# FIXME: Move to fnpdjango
import feedparser
import datetime
@register.inclusion_tag('catalogue/latest_blog_posts.html')
def latest_blog_posts(feed_url, posts_to_show=5):
    try:
        feed = feedparser.parse(str(feed_url))
        posts = []
        for i in range(posts_to_show):
            pub_date = feed['entries'][i].updated_parsed
            published = datetime.date(pub_date[0], pub_date[1], pub_date[2] )
            posts.append({
                'title': feed['entries'][i].title,
                'summary': feed['entries'][i].summary,
                'link': feed['entries'][i].link,
                'date': published,
                })
        return {'posts': posts}
    except:
        return {'posts': []}
