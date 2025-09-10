from django import template
from django.contrib.humanize.templatetags.humanize import intcomma

register = template.Library()


@register.filter
def format_price(value):
    """Format price with 2 decimal places and commas"""
    try:
        # Convert to float, format to 2 decimal places, then add commas
        formatted = "{:.2f}".format(float(value))
        return intcomma(formatted)
    except (ValueError, TypeError):
        return value
