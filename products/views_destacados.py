from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.contrib.admin.views.decorators import staff_member_required
from django.views.decorators.http import require_POST
from .models import Producto

@staff_member_required
@require_POST
def toggle_destacado(request, producto_id):
    """Vista para alternar el estado destacado de un producto"""
    producto = get_object_or_404(Producto, id=producto_id)

    # Debug para ver si la vista se ejecuta y el usuario es staff
    print(f"[DEBUG] toggle_destacado ejecutado para producto_id={producto_id}")
    print(f"[DEBUG] Usuario: {request.user}, is_staff: {request.user.is_staff}")
    print(f"[DEBUG] Estado antes: {producto.destacado}")

    # Alternar el estado
    producto.destacado = not producto.destacado
    producto.save()

    print(f"[DEBUG] Estado después: {producto.destacado}")

    return JsonResponse({
        'success': True,
        'destacado': producto.destacado,
        'message': f'Producto {"destacado" if producto.destacado else "no destacado"}'
    })
