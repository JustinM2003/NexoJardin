from django.urls import path
from . import views
from .views_search import buscar_productos
from django.contrib.auth.views import LoginView, LogoutView

urlpatterns = [
    path('', views.home, name='home'),
    path('plantas/', views.plantas, name='plantas'),
    path('materiales/', views.materiales, name='materiales'),
    path('informacion/', views.informacion, name='informacion'),
    path('ver-todo/', views.mantencion, name='ver-todo'),
    path('producto/<int:id>/', views.detalle_producto, name='detalle_producto'),
    path('api/buscar/', buscar_productos, name='buscar_productos'),
    path('nosotros/', views.nosotros, name='nosotros'),
    path('login/', LoginView.as_view(template_name='login.html', next_page='/'), name='login'),
    path('logout/', LogoutView.as_view(next_page='/'), name='logout'),
]
