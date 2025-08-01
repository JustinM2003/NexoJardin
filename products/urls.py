from django.urls import path 
from . import views 
from .views_destacados import toggle_destacado


urlpatterns = [
    path('agregar/', views.agregar_producto, name='agregar_producto'),
    path('editar/<int:producto_id>/', views.editar_producto, name='editar_producto'),
    path('eliminar/<int:producto_id>/', views.eliminar_producto, name='eliminar_producto'),
    path('editar-descripciones/<int:producto_id>/', views.editar_descripciones, name='editar_descripciones'),
    path('agregar-categoria/', views.agregar_categoria, name='agregar_categoria'),
    path('eliminar-categoria/', views.eliminar_categoria, name='eliminar_categoria'),
    path('toggle-destacado/<int:producto_id>/', toggle_destacado, name='toggle_destacado'),
]