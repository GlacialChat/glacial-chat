from django import template
from re import sub

register = template.Library()


@register.filter
def norm_name(name):
    return sub(r"(.+[\\/])?(\w+)(_\w{0,7})(\.\w+)?$", r"\2\4", name)
