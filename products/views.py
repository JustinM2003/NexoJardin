
from django.contrib.auth.decorators import user_passes_test
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from .models import Producto, Categoria
from .forms import ProductoForm, CategoriaForm

from django.http import JsonResponse

@user_passes_test(lambda u: u.is_staff)
def eliminar_categoria(request, categoria_id=None):
    if request.method == 'POST':
        cat_id = request.POST.get('categoria_id') or categoria_id
        if cat_id:
            try:
                categoria = Categoria.objects.get(id=cat_id)
                categoria.delete()
            except Categoria.DoesNotExist:
                pass
        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            # Filtrar categorías por tipo si se especifica
            tipo = request.GET.get('tipo') or request.POST.get('tipo')
            if tipo:
                categorias = list(Categoria.objects.filter(tipo=tipo).values('id', 'nombre'))
            else:
                categorias = list(Categoria.objects.values('id', 'nombre'))
            return JsonResponse({'categorias': categorias})
    elif request.headers.get('x-requested-with') == 'XMLHttpRequest':
        # Filtrar categorías por tipo si se especifica
        tipo = request.GET.get('tipo') or request.POST.get('tipo')
        if tipo:
            categorias = list(Categoria.objects.filter(tipo=tipo).values('id', 'nombre'))
        else:
            categorias = list(Categoria.objects.values('id', 'nombre'))
        return JsonResponse({'categorias': categorias})
    return redirect('plantas')

@user_passes_test(lambda u: u.is_staff)
def agregar_categoria(request):
    tipo = request.GET.get('tipo') or request.POST.get('tipo')
    if request.method == 'POST':
        form = CategoriaForm(request.POST)
        if form.is_valid():
            categoria = form.save(commit=False)
            if tipo in ['planta', 'material']:
                categoria.tipo = tipo
            categoria.save()
            if request.headers.get('x-requested-with') == 'XMLHttpRequest':
                # Filtrar categorías por tipo si se especifica
                if tipo:
                    categorias = list(Categoria.objects.filter(tipo=tipo).values('id', 'nombre'))
                else:
                    categorias = list(Categoria.objects.values('id', 'nombre'))
                return JsonResponse({'success': True, 'id': categoria.id, 'nombre': categoria.nombre, 'tipo': categoria.tipo, 'categorias': categorias})
            return redirect(tipo if tipo else 'plantas')
        else:
            # Si el formulario no es válido, devolver la lista actualizada igual
            if request.headers.get('x-requested-with') == 'XMLHttpRequest':
                # Filtrar categorías por tipo si se especifica
                if tipo:
                    categorias = list(Categoria.objects.filter(tipo=tipo).values('id', 'nombre'))
                else:
                    categorias = list(Categoria.objects.values('id', 'nombre'))
                return JsonResponse({'success': False, 'categorias': categorias})
    else:
        form = CategoriaForm()
    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        # Filtrar categorías por tipo si se especifica
        if tipo:
            categorias = list(Categoria.objects.filter(tipo=tipo).values('id', 'nombre'))
        else:
            categorias = list(Categoria.objects.values('id', 'nombre'))
        return JsonResponse({'categorias': categorias})
    return redirect(tipo if tipo else 'plantas')

@user_passes_test(lambda u: u.is_staff)
def agregar_producto(request):
    tipo = request.GET.get('tipo') or request.POST.get('tipo')
    if request.method == 'POST':
        form = ProductoForm(request.POST, request.FILES)
        if form.is_valid():
            from decimal import Decimal
            producto = form.save(commit=False)
            producto.precio = producto.precio * Decimal('1.3')
            if tipo in ['planta', 'material']:
                producto.tipo = tipo
            categoria_id = request.POST.get('categoria')
            if categoria_id:
                from products.models import Categoria
                try:
                    producto.categoria = Categoria.objects.get(id=categoria_id)
                except Categoria.DoesNotExist:
                    producto.categoria = None
            producto.save()
            if request.headers.get('x-requested-with') == 'XMLHttpRequest':
                return JsonResponse({'success': True, 'id': producto.id, 'nombre': producto.nombre, 'tipo': producto.tipo})
            return redirect(tipo if tipo else 'plantas')
    else:
        form = ProductoForm()
    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        return JsonResponse({'success': False})
    return render(request, 'products/agregar_producto.html', {'form': form, 'tipo': tipo})

@user_passes_test(lambda u: u.is_staff)
def eliminar_producto(request, producto_id):
    producto = get_object_or_404(Producto, id=producto_id)
    if request.method == 'POST':
        producto.delete()
        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            return JsonResponse({'success': True})
        return redirect('plantas')

# FUNCIÓN AGREGAR PRODUCTO (sin incremento del 30%)
@user_passes_test(lambda u: u.is_staff)
def agregar_producto(request):
    tipo = request.GET.get('tipo') or request.POST.get('tipo')
    if request.method == 'POST':
        form = ProductoForm(request.POST, request.FILES)
        if form.is_valid():
            producto = form.save(commit=False)
            # ELIMINADO: producto.precio = producto.precio * Decimal('1.3')
            # Ahora el precio se guarda tal como se ingresa
            if tipo in ['planta', 'material']:
                producto.tipo = tipo
            categoria_id = request.POST.get('categoria')
            if categoria_id:
                from products.models import Categoria
                try:
                    producto.categoria = Categoria.objects.get(id=categoria_id)
                except Categoria.DoesNotExist:
                    producto.categoria = None
            producto.save()
            if request.headers.get('x-requested-with') == 'XMLHttpRequest':
                return JsonResponse({'success': True, 'id': producto.id, 'nombre': producto.nombre, 'tipo': producto.tipo})
            return redirect(tipo if tipo else 'plantas')
    else:
        form = ProductoForm()
    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        return JsonResponse({'success': False})
    return render(request, 'products/agregar_producto.html', {'form': form, 'tipo': tipo})

# FUNCIÓN EDITAR PRODUCTO (sin incremento del 30%)
@user_passes_test(lambda u: u.is_staff)
def editar_producto(request, producto_id):
    producto = get_object_or_404(Producto, id=producto_id)
    from decimal import Decimal, ROUND_HALF_UP
    tipo = producto.tipo
    
    if request.method == 'POST':
        form = ProductoForm(request.POST, request.FILES, instance=producto)
        if form.is_valid():
            producto_editado = form.save(commit=False)
            
            # Verificar si se debe eliminar la imagen
            eliminar_imagen = request.POST.get('eliminar_imagen') == 'true'
            if eliminar_imagen:
                if producto_editado.imagen:
                    producto_editado.imagen.delete(save=False)
                producto_editado.imagen = None
            
            # SIMPLIFICADO: Ya no hay lógica compleja de precios
            # El precio del formulario se aplica directamente
            producto_editado.precio = form.cleaned_data['precio']
                
            # Asignar categoría
            producto_editado.categoria = form.cleaned_data.get('categoria')
            
            # Guardar
            producto_editado.save()
            
            if request.headers.get('x-requested-with') == 'XMLHttpRequest':
                return JsonResponse({'success': True})
            return redirect('plantas' if tipo == 'planta' else 'materiales')
        else:
            # Si hay errores en el formulario, mostrarlos
            if request.headers.get('x-requested-with') == 'XMLHttpRequest':
                return render(request, 'products/editar_producto_form.html', {
                    'form': form, 
                    'producto': producto,
                    'precio_base_original': producto.precio  # Ahora es el precio real
                })
    else:
        # GET request
        form = ProductoForm(instance=producto)
        # Ya no calculamos precio base, usamos el precio real
        form.fields['precio'].initial = producto.precio
        form.fields['categoria'].queryset = Categoria.objects.filter(tipo=tipo)
    
    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        return render(request, 'products/editar_producto_form.html', {
            'form': form, 
            'producto': producto,
            'precio_base_original': producto.precio  # Precio real del producto
        })
    return render(request, 'products/editar_producto.html', {'form': form, 'producto': producto})

@user_passes_test(lambda u: u.is_staff)
@require_POST
def editar_descripciones(request, producto_id):
    """Vista para editar solo las descripciones de un producto via AJAX"""
    try:
        producto = get_object_or_404(Producto, id=producto_id)
        
        # Obtener los nuevos valores de las descripciones
        descripcion_corta = request.POST.get('descripcion_corta', '').strip()
        descripcion = request.POST.get('descripcion', '').strip()
        
        # Actualizar el producto
        producto.descripcion_corta = descripcion_corta if descripcion_corta else None
        producto.descripcion = descripcion if descripcion else None
        producto.save()
        
        return JsonResponse({
            'success': True,
            'descripcion_corta': descripcion_corta,
            'descripcion': descripcion
        })
        
    except Exception as e:
        return JsonResponse({
            'success': False,
            'error': str(e)
        })