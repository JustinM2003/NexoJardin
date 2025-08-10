from django import template
from django.conf import settings

register = template.Library()

@register.simple_tag(takes_context=True)
def absolute_url(context, url_name, *args, **kwargs):
    """
    Genera una URL absoluta para uso en meta tags SEO
    """
    from django.urls import reverse
    request = context['request']
    relative_url = reverse(url_name, args=args, kwargs=kwargs)
    return request.build_absolute_uri(relative_url)

@register.simple_tag(takes_context=True)
def site_url(context):
    """
    Obtiene la URL base del sitio
    """
    request = context['request']
    return f"{request.scheme}://{request.get_host()}"
