from django.contrib.sitemaps import Sitemap
from django.urls import reverse
from products.models import Producto

class StaticViewSitemap(Sitemap):
    """Sitemap para páginas estáticas"""
    priority = 0.5
    changefreq = 'daily'

    def items(self):
        return ['home', 'ver-todo', 'plantas', 'materiales']

    def location(self, item):
        return reverse(item)

class ProductoSitemap(Sitemap):
    """Sitemap para productos"""
    changefreq = "daily"
    priority = 0.8

    def items(self):
        return Producto.objects.all()

    def lastmod(self, obj):
        # Si tienes un campo de última modificación, úsalo aquí
        # return obj.fecha_modificacion
        return None

    def location(self, obj):
        return reverse('detalle_producto', args=[obj.pk])

# Diccionario de todos los sitemaps
sitemaps = {
    'static': StaticViewSitemap,
    'productos': ProductoSitemap,
}
