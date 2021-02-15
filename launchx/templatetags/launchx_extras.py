from django import template
from django.conf import settings

register = template.Library()

@register.simple_tag
def static(file_location):
    return settings.STATIC_PREFIX + file_location