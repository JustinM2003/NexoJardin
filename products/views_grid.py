from django.shortcuts import render
from .models import Producto, Categoria
from .forms import ProductoForm, CategoriaForm

def productos_grid(request, tipo):
    # Filtrar productos y categorías por tipo
    productos = Producto.objects.filter(tipo=tipo)
    categorias = Categoria.objects.filter(tipo=tipo)
    titulo = 'Plantas' if tipo == 'planta' else 'Materiales'
    # Formularios
    producto_form = ProductoForm()
    categoria_form = CategoriaForm()
    # URLs para modales y acciones
    context = {
        'productos': productos,
        'categorias': categorias,
        'titulo': titulo,
        'tipo': tipo,
        'producto_form': producto_form,
        'categoria_form': categoria_form,
        'agregar_producto_url': 'agregar_producto',
        'agregar_categoria_url': 'agregar_categoria',
        'eliminar_categoria_url': 'eliminar_categoria',
        'detalle_producto_url': 'detalle_producto',
    }
    return render(request, 'products/productos_grid.html', context)
