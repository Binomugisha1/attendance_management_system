from django import template
register = template.Library()

@register.filter
def get_value(obj, name):
    val = getattr(obj, name, '')
    return '' if val is None else val
