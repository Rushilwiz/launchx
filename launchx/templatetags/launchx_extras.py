from django import template
from django.conf import settings

register = template.Library()

@register.simple_tag
def static(file_location):
    return settings.STATIC_PREFIX + file_location

@register.simple_tag
def url(url):
    if url[-1] == '/':
        return settings.URL_PREFIX + url
    else:
        return settings.URL_PREFIX + url + '/'