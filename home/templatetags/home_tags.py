from django import template

register = template.Library()


@register.filter
def multiply(value, num):
    return (value-1)*num


@register.filter
def min(value, num):
    return int(value)-num