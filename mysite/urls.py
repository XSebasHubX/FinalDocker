"""
URL configuration for your Django app.
"""

from django.urls import path, include
from . import views


urlpatterns = [
    path('', views.inicio, name='inicio'),  # Ruta raíz ahora apunta a inicio
    path('index/', views.index, name='index'),
    path('profile/', views.profile, name='profile'),
    path('', include('social_django.urls')),
    path('logout/', views.logout, name='logout'),
    path('inventario/', views.inventario_view, name='inventario'),
]
