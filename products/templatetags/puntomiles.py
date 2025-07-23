
from django import template

register = template.Library()

def puntomiles(value):
    try:
        value = int(float(value))
    except (ValueError, TypeError):
        return value
    return f"{value:,}".replace(",", ".")

register.filter('puntomiles', puntomiles)

