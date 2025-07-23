
from django.contrib.auth.decorators import user_passes_test
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
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
                # Eliminar la imagen del producto
                if producto_editado.imagen:
                    producto_editado.imagen.delete(save=False)
                producto_editado.imagen = None
            
            # Normalizar el valor del precio (coma a punto)
            nuevo_precio_raw = str(form.cleaned_data['precio'])
            nuevo_precio = nuevo_precio_raw.replace(',', '.')
            nuevo_precio_decimal = Decimal(nuevo_precio).quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)
            
            # Calcular el precio base actual (sin el 30%)
            precio_base_actual = (Decimal(producto.precio) / Decimal('1.3')).quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)
            
            # Comparar si el precio base cambió
            if nuevo_precio_decimal == precio_base_actual:
                # El precio base NO cambió, mantener el precio actual (ya tiene el 30% aplicado)
                producto_editado.precio = producto.precio
            else:
                # El precio base SÍ cambió, aplicar el 30% al nuevo precio base
                producto_editado.precio = nuevo_precio_decimal * Decimal('1.3')
                
            # Asignar categoría usando cleaned_data
            producto_editado.categoria = form.cleaned_data.get('categoria')
            producto_editado.save()
            if request.headers.get('x-requested-with') == 'XMLHttpRequest':
                return JsonResponse({'success': True})
            return redirect('plantas' if tipo == 'planta' else 'materiales')
    else:
        # IMPORTANTE: Mostrar siempre el precio base (sin el 30%) en el formulario
        precio_base = (Decimal(producto.precio) / Decimal('1.3')).quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)
        form = ProductoForm(instance=producto)
        form.fields['precio'].initial = precio_base
        # Filtrar categorías por tipo
        form.fields['categoria'].queryset = Categoria.objects.filter(tipo=tipo)
    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        # Calcular el precio base para pasarlo al template
        precio_base = (Decimal(producto.precio) / Decimal('1.3')).quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)
        return render(request, 'products/editar_producto_form.html', {
            'form': form, 
            'producto': producto,
            'precio_base_original': precio_base
        })
    return render(request, 'products/editar_producto.html', {'form': form, 'producto': producto})
