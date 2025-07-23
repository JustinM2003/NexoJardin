from django.shortcuts import render, get_object_or_404
from django.views.generic import TemplateView
from products.models import Producto

# Create your views here.

class HomePageView(TemplateView):
    template_name = "pages/home.html"

def home(request):
    # Obtener productos destacados para mostrar en el carrusel
    productos_destacados = Producto.objects.filter(destacado=True)[:10]  # Máximo 8 productos destacados
    return render(request, 'pages/home.html', {
        'productos_destacados': productos_destacados
    })

def plantas(request):
    from products.forms import ProductoForm, CategoriaForm
    from products.models import Producto, Categoria
    productos = Producto.objects.filter(tipo='planta')
    categorias = Categoria.objects.filter(tipo='planta')
    # Filtros
    categoria_id = request.GET.get('categoria')
    if categoria_id:
        productos = productos.filter(categoria_id=categoria_id)
    orden_precio = request.GET.get('orden_precio')
    if orden_precio == 'menor':
        productos = productos.order_by('precio')
    elif orden_precio == 'mayor':
        productos = productos.order_by('-precio')
    producto_form = ProductoForm()
    categoria_form = CategoriaForm()
    return render(request, 'productos.html', {
        'productos': productos,
        'categorias': categorias,
        'producto_form': producto_form,
        'categoria_form': categoria_form,
        'tipo': 'planta',
        'titulo': 'Plantas',
        'agregar_producto_url': 'agregar_producto',
        'agregar_categoria_url': 'agregar_categoria',
        'eliminar_categoria_url': 'eliminar_categoria',
        'detalle_producto_url': 'detalle_producto',
    })

def materiales(request):
    from products.forms import ProductoForm, CategoriaForm
    from products.models import Producto, Categoria
    productos = Producto.objects.filter(tipo='material')
    categorias = Categoria.objects.filter(tipo='material')
    # Filtros
    categoria_id = request.GET.get('categoria')
    if categoria_id:
        productos = productos.filter(categoria_id=categoria_id)
    orden_precio = request.GET.get('orden_precio')
    if orden_precio == 'menor':
        productos = productos.order_by('precio')
    elif orden_precio == 'mayor':
        productos = productos.order_by('-precio')
    producto_form = ProductoForm()
    categoria_form = CategoriaForm()
    return render(request, 'productos.html', {
        'productos': productos,
        'categorias': categorias,
        'producto_form': producto_form,
        'categoria_form': categoria_form,
        'tipo': 'material',
        'titulo': 'Materiales',
        'agregar_producto_url': 'agregar_producto',
        'agregar_categoria_url': 'agregar_categoria',
        'eliminar_categoria_url': 'eliminar_categoria',
        'detalle_producto_url': 'detalle_producto',
    })

def informacion(request):
    return render(request, 'pages/informacion.html')

def mantencion(request):
    from products.forms import ProductoForm, CategoriaForm
    from products.models import Producto, Categoria
    from django.db.models import Q
    
    # Obtener todos los productos (plantas y materiales)
    productos = Producto.objects.all()
    
    # Obtener todas las categorías separadas por tipo
    categorias_plantas = Categoria.objects.filter(tipo='planta')
    categorias_materiales = Categoria.objects.filter(tipo='material')
    
    # Manejar búsqueda desde la barra de búsqueda
    query = request.GET.get('q', '').strip()
    if query:
        # Si es un solo carácter, buscar productos que empiecen con esa letra
        if len(query) == 1:
            productos = productos.filter(Q(nombre__istartswith=query))
        else:
            # Para múltiples caracteres, buscar que contengan el texto
            productos = productos.filter(Q(nombre__icontains=query) | Q(descripcion__icontains=query))
    
    # Aplicar filtros si existen
    categoria_id = request.GET.get('categoria')
    if categoria_id:
        productos = productos.filter(categoria_id=categoria_id)
    
    tipo_filtro = request.GET.get('tipo')
    if tipo_filtro:
        productos = productos.filter(tipo=tipo_filtro)
    
    orden_precio = request.GET.get('orden_precio')
    if orden_precio == 'menor':
        productos = productos.order_by('precio')
    elif orden_precio == 'mayor':
        productos = productos.order_by('-precio')
    else:
        # Mantener orden por ID (plantas prioritarias primero)
        productos = productos.order_by('id')
    
    producto_form = ProductoForm()
    categoria_form = CategoriaForm()
    
    # Determinar el título basado en si hay búsqueda
    if query:
        titulo = f'Resultados para: "{query}"'
        total_resultados = productos.count()
    else:
        titulo = 'Ver Todo'
        total_resultados = productos.count()
    
    return render(request, 'productos.html', {
        'productos': productos,
        'categorias': categorias_plantas.union(categorias_materiales),  # Todas las categorías
        'categorias_plantas': categorias_plantas,
        'categorias_materiales': categorias_materiales,
        'producto_form': producto_form,
        'categoria_form': categoria_form,
        'tipo': 'todos',  # Indicador especial para "ver todo"
        'titulo': titulo,
        'query': query,  # Pasar la búsqueda al template
        'total_resultados': total_resultados,
        'agregar_producto_url': 'agregar_producto',
        'agregar_categoria_url': 'agregar_categoria',
        'eliminar_categoria_url': 'eliminar_categoria',
        'detalle_producto_url': 'detalle_producto',
    })

def detalle_producto(request, id):
    producto = get_object_or_404(Producto, id=id)
    return render(request, 'pages/detalle_producto.html', {'producto': producto})