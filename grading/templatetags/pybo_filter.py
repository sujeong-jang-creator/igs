from django import template

register = template.Library()


@register.filter
def sub(value, arg):
    return value - arg

@register.filter
def multi(value, arg):
    return value * arg