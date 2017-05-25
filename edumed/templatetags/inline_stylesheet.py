# -*- coding: utf-8 -*-
# https://github.com/jazzband/django-pipeline/issues/295#issuecomment-152095865
# adjusted for older pipeline
from __future__ import unicode_literals
import codecs

from django.contrib.staticfiles.storage import staticfiles_storage
from django.utils.safestring import mark_safe
from django import template
from pipeline.templatetags import compressed

register = template.Library()


class StylesheetNode(compressed.CompressedCSSNode):
    def render_css(self, package, path):
        return self.render_individual_css(package, [path])

    def render_individual_css(self, package, paths, **kwargs):
        html = []
        for path in paths:
            with codecs.open(staticfiles_storage.path(path), 'r', 'utf-8') as f:
                html.append(f.read())
        html = '<style type="text/css">' + '\n'.join(html) + '</style>'
        return mark_safe(html)


@register.tag
def inline_stylesheet(parser, token):
    """ Template tag that mimics pipeline's stylesheet tag, but embeds
    the resulting CSS directly in the page.
    """
    try:
        tag_name, name = token.split_contents()
    except ValueError:
        raise template.TemplateSyntaxError(
            '%r requires exactly one argument: the name of a group in the PIPELINE_CSS setting'
            % token.split_contents()[0])
    return StylesheetNode(name)
