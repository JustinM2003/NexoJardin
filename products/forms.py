from django import forms
from .models import Producto, Categoria


class ProductoForm(forms.ModelForm):
    class Meta:
        model = Producto
        fields = ['nombre', 'descripcion', 'descripcion_corta', 'medidas', 'precio_base', 'porcentaje_extra', 'incluir_iva', 'imagen', 'categoria']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['descripcion'].required = False
        self.fields['descripcion_corta'].required = False
        self.fields['medidas'].required = False
        self.fields['porcentaje_extra'].required = False
        
        # Personalizar labels y help texts
        self.fields['precio_base'].label = 'Precio base'
        self.fields['precio_base'].help_text = 'Precio sin IVA ni porcentajes adicionales'
        self.fields['porcentaje_extra'].label = 'Porcentaje extra (%)'
        self.fields['porcentaje_extra'].help_text = 'Porcentaje adicional a aplicar (ej: 30 para 30%)'
        self.fields['incluir_iva'].label = 'Incluir IVA (19%)'

class CategoriaForm(forms.ModelForm):
    class Meta:
        model = Categoria
        fields = ['nombre']
