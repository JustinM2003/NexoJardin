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
    descripcion_corta= models.TextField(blank=True, null=True)
    medidas = models.TextField(blank=True, null=True)
    precio_base = models.DecimalField(max_digits=10, decimal_places=2)  # Precio sin modificaciones
    porcentaje_extra = models.DecimalField(max_digits=5, decimal_places=2, default=0, blank=True)  # Porcentaje adicional
    incluir_iva = models.BooleanField(default=False)  # Si incluir IVA del 19%
    precio = models.DecimalField(max_digits=10, decimal_places=2)  # Precio final calculado
    imagen = models.ImageField(upload_to='productos/', blank=True, null=True)
    categoria = models.ForeignKey(Categoria, on_delete=models.CASCADE, blank=True, null=True)
    tipo = models.CharField(max_length=10, choices=TIPO_CHOICES, default='planta')
    destacado = models.BooleanField(default=False)  # Nuevo campo para productos destacados

    def __str__(self):
        return self.nombre

    def calcular_precio_final(self):
        """Calcula el precio final basado en precio_base, porcentaje_extra e IVA"""
        from decimal import Decimal
        precio = self.precio_base
        
        # Aplicar porcentaje extra
        if self.porcentaje_extra > 0:
            precio = precio * (1 + self.porcentaje_extra / 100)
        
        # Aplicar IVA si está marcado
        if self.incluir_iva:
            precio = precio * Decimal('1.19')  # 19% de IVA
            
        return precio.quantize(Decimal('0.01'))  # Redondear a 2 decimales
    
    def save(self, *args, **kwargs):
        """Override save para calcular automáticamente el precio final"""
        self.precio = self.calcular_precio_final()
        super().save(*args, **kwargs)

    def get_imagen_url(self):
        if self.imagen:
            return self.imagen.url
        return '/media/productos/default.jpg'  # Ajusta la ruta según tu configuración
    

    