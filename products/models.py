from django.db import models

# Create your models here.


class Categoria(models.Model):
    TIPO_CHOICES = [
        ('planta', 'Planta'),
        ('material', 'Material'),
    ]
    nombre = models.CharField(max_length=100)
    tipo = models.CharField(max_length=10, choices=TIPO_CHOICES, default='planta')

    def __str__(self):
        return self.nombre

class Producto(models.Model):
    TIPO_CHOICES = [
        ('planta', 'Planta'),
        ('material', 'Material'),
    ]
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField(blank=True, null=True)
    precio = models.DecimalField(max_digits=10, decimal_places=2)
    imagen = models.ImageField(upload_to='productos/', blank=True, null=True)
    categoria = models.ForeignKey(Categoria, on_delete=models.CASCADE, blank=True, null=True)
    tipo = models.CharField(max_length=10, choices=TIPO_CHOICES, default='planta')
    destacado = models.BooleanField(default=False)  # Nuevo campo para productos destacados

    def __str__(self):
        return self.nombre

    def get_imagen_url(self):
        if self.imagen:
            return self.imagen.url
        return '/media/productos/default.jpg'  # Ajusta la ruta según tu configuración
    

    