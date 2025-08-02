from django import forms
from .models import Producto, Categoria


class ProductoForm(forms.ModelForm):
    class Meta:
        model = Producto
        fields = ['nombre', 'descripcion', 'descripcion_corta', 'medidas', 'precio', 'imagen', 'categoria']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['descripcion'].required = False
        self.fields['descripcion_corta'].required = False
        self.fields['medidas'].required = False

class CategoriaForm(forms.ModelForm):
    class Meta:
        model = Categoria
        fields = ['nombre']
