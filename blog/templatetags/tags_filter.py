from django import template
from django.template.defaultfilters import stringfilter

register = template.Library()


@register.filter()
@stringfilter
def splitter(value):
    return [x.strip().capitalize() for x in value.split(",")]
