from django.http import JsonResponse
from django.db.models import Q
from products.models import Producto

def buscar_productos(request):
    """Vista para búsqueda en tiempo real de productos"""
    query = request.GET.get('q', '').strip()
    
    # Debug: Imprimir la consulta recibida
    print(f"Búsqueda recibida: '{query}'")
    
    if len(query) < 1:  # Solo buscar si hay al menos 1 carácter
        return JsonResponse({'productos': []})
    
    # Buscar productos que coincidan en nombre o descripción
    # Si es un solo carácter, buscar productos que empiecen con esa letra
    if len(query) == 1:
        productos = Producto.objects.filter(
            Q(nombre__istartswith=query)
        )[:10]
    else:
        # Para múltiples caracteres, buscar que contengan el texto
        productos = Producto.objects.filter(
            Q(nombre__icontains=query) | Q(descripcion__icontains=query)
        )[:10]
    
    # Debug: Imprimir cantidad de resultados
    print(f"Productos encontrados: {productos.count()}")
    
    # Preparar datos para JSON
    resultados = []
    for producto in productos:
        resultados.append({
            'id': producto.id,
            'nombre': producto.nombre,
            'precio': str(producto.precio),
            'imagen_url': producto.imagen.url if producto.imagen else '/static/img/default.jpg'
        })
    
    return JsonResponse({'productos': resultados})
