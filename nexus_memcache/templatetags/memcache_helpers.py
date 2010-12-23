from django import template
from django.contrib.humanize.templatetags.humanize import intcomma

import datetime

register = template.Library()

def humanize_bytes(bytes):
    bytes = float(bytes)
    if bytes >= 1073741824:
        gigabytes = bytes / 1073741824
        size = '%.2fGB' % gigabytes
    elif bytes >= 1048576:
        megabytes = bytes / 1048576
        size = '%.2fMB' % megabytes
    elif bytes >= 1024:
        kilobytes = bytes / 1024
        size = '%.2fKB' % kilobytes
    else:
        size = '%.2fB' % bytes
    return size
register.filter(humanize_bytes)

register.filter(intcomma)

def duration(value):
    from django.template.defaultfilters import timesince
    value = datetime.datetime.now() - datetime.timedelta(seconds=int(value))
    return timesince(value)
register.filter(duration)

register.filter('int', lambda x: int(x))