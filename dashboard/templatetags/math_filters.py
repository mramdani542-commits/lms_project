# dashboard/templatetags/math_filters.py

from django import template

register = template.Library()

@register.filter
def div(value, arg):
    try:
        # Pastikan pembagi tidak nol
        if float(arg) == 0:
            return 0
        return float(value) / float(arg)
    except (ValueError, TypeError):
        return 0

@register.filter
def mul(value, arg):
    try:
        return float(value) * float(arg)
    except (ValueError, TypeError):
        return 0