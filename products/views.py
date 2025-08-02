from django.contrib.auth.decorators import user_passes_test
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.contrib import messages
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


# --- Vista para editar producto completo por AJAX ---
@user_passes_test(lambda u: u.is_staff)
def editar_producto(request, producto_id):
    """Vista para editar producto completo por AJAX"""
    producto = get_object_or_404(Producto, id=producto_id)
    
    if request.method == 'GET' and request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        # Retornar el formulario para editar
        from .forms import ProductoForm
        form = ProductoForm(instance=producto)
        # Filtrar categorías por tipo
        form.fields['categoria'].queryset = Categoria.objects.filter(tipo=producto.tipo)
        
        # Precio original para mostrar en el formulario
        precio_base_original = producto.precio
        
        return render(request, 'products/editar_producto_form.html', {
            'form': form,
            'producto': producto,
            'precio_base_original': precio_base_original
        })
    
    elif request.method == 'POST':
        # Procesar la edición
        from .forms import ProductoForm
        form = ProductoForm(request.POST, request.FILES, instance=producto)
        
        # Filtrar categorías por tipo
        form.fields['categoria'].queryset = Categoria.objects.filter(tipo=producto.tipo)
        
        if form.is_valid():
            # Verificar si se debe eliminar la imagen
            eliminar_imagen = request.POST.get('eliminar_imagen') == 'true'
            if eliminar_imagen and producto.imagen:
                producto.imagen.delete()
                producto.imagen = None
            
            producto_editado = form.save()
            
            if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                return JsonResponse({
                    'success': True,
                    'message': 'Producto editado exitosamente'
                })
            else:
                messages.success(request, 'Producto editado exitosamente')
                return redirect('productos')
        else:
            if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                errors = []
                for field, field_errors in form.errors.items():
                    for error in field_errors:
                        errors.append(f"{field}: {error}")
                return JsonResponse({
                    'success': False,
                    'errors': errors
                })
            else:
                return render(request, 'products/editar_producto_form.html', {
                    'form': form,
                    'producto': producto
                })
    
    return JsonResponse({'success': False, 'error': 'Método no permitido'})


# --- Vista para editar producto inline por AJAX ---
@user_passes_test(lambda u: u.is_staff)
@require_POST
def editar_descripciones(request, producto_id):
    """Vista para editar producto inline por AJAX"""
    producto = get_object_or_404(Producto, id=producto_id)
    try:
        nombre = request.POST.get('nombre', '').strip()
        precio_base = request.POST.get('precio_base', '').strip()
        porcentaje_extra = request.POST.get('porcentaje_extra', '').strip()
        incluir_iva = request.POST.get('incluir_iva') == 'on'
        descripcion_corta = request.POST.get('descripcion_corta', '').strip()
        descripcion = request.POST.get('descripcion', '').strip()
        medidas = request.POST.get('medidas', '').strip()
        imagen = request.FILES.get('imagen')

        if nombre:
            producto.nombre = nombre
        if precio_base:
            from decimal import Decimal
            try:
                producto.precio_base = Decimal(precio_base)
            except Exception:
                pass
        if porcentaje_extra:
            from decimal import Decimal
            try:
                producto.porcentaje_extra = Decimal(porcentaje_extra)
            except Exception:
                pass
        else:
            producto.porcentaje_extra = 0
            
        producto.incluir_iva = incluir_iva
        producto.descripcion_corta = descripcion_corta if descripcion_corta else None
        producto.descripcion = descripcion if descripcion else None
        producto.medidas = medidas if medidas else None
        if imagen:
            producto.imagen = imagen
        producto.save()  # Esto calculará automáticamente el precio final
        return JsonResponse({'success': True})
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)})
    
