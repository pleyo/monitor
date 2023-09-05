import datetime
import humanize
from django import template

register = template.Library()

@register.filter
def get_obj_attr(obj, attr):
    try:
        return obj[str(attr)]
    except Exception as err:
        return None

@register.filter()
def timestamp_to_date(obj):
    return datetime.datetime.fromtimestamp(int(obj))

@register.filter()
def naturaldelta(obj):
    return humanize.naturaldelta(obj)
