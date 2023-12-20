from django import template
from django.utils import timesince
from django.utils.html import format_html

register = template.Library()


@register.filter(name='simplify_timesince')
def simplify_timesince(value):
    simplified_timesince = timesince.timesince(value)
    parts = simplified_timesince.split(', ')
    if len(parts) > 1:
        return format_html('{}', parts[0])
    return format_html('{}', simplified_timesince)