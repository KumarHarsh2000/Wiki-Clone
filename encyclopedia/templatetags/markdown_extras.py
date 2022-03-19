from django import template
from django.template.defaultfilters import stringfilter

import markdown as encyclopedia

register = template.Library()


@register.filter()
@stringfilter
def markdown(value):
    return encyclopedia.markdown(value, extensions=['markdown.extensions.fenced_code'])