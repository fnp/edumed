from django import template
from django.utils.datastructures import SortedDict
from ..models import Lesson, Section

register = template.Library()


@register.inclusion_tag("catalogue/snippets/carousel.html")
def catalogue_carousel():
    return {
    }

@register.inclusion_tag("catalogue/snippets/section_buttons.html")
def catalogue_section_buttons():
    return {
        "object_list": Section.objects.all()
    }

@register.inclusion_tag("catalogue/snippets/chosen_topics.html")
def catalogue_chosen_topics():
    return {
    }

@register.inclusion_tag("catalogue/snippets/section_box.html")
def section_box(section):
    lessons = SortedDict()
    for lesson in section.lesson_set.all():
        if lesson.level not in lessons:
            newdict = SortedDict()
            newdict['synthetic'] = []
            newdict['course'] = []
            lessons[lesson.level] = newdict
        if lesson.type not in lessons[lesson.level]:
            lessons[lesson.level][lesson.type] = []
        lessons[lesson.level][lesson.type].append(lesson)
    return {
        "lessons": lessons,
    }

@register.inclusion_tag("catalogue/snippets/lesson_nav.html")
def lesson_nav(lesson):
    if lesson.type == 'course':
        root = lesson.section
        siblings = root.lesson_set.filter(type='course')
    else:
        root = None
        siblings = Lesson.objects.filter(type=lesson.type)
    return {
        "lesson": lesson,
        "root": root,
        "siblings": siblings,
    }

@register.filter
def person_list(persons):
    from librarian.dcparser import Person
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
