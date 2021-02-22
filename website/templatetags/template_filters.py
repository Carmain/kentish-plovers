from django import template
from website.models import SEX_CHOICES, COLOR_CHOICES

register = template.Library()


@register.filter
def sex_to_string(value):
    for choice in SEX_CHOICES:
        if choice[0] == value:
            return choice[1]

    return None


@register.filter
def color_to_string(value):
    for choice in COLOR_CHOICES:
        if choice[0] == value:
            return choice[1]

    return None
