# from urllib.parse import quote_plus # Python 3.x
from urllib import quote_plus # Python 2.x
from django import template

register = template.Library()

@register.filter
def urlify(value):
    return quote_plus(value)
