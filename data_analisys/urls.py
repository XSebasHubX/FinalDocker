from django.urls import path
from django.contrib.auth.views import LogoutView
from . import views

urlpatterns = [
    path('inventario/', views.inventario_view, name='inventario'),
    path('data_analisys/dashboard/', views.ventas_dashboard, name='dashboard'),
    path('data_analisys/AnalisisRegional/', views.analisis_regional, name='AnalisisRegional'),
    path('data_analisys/DesempeñoProducto/', views.desempeno_producto, name='DesempeñoProducto'),
    path('data_analisys/TendenciasComparativas/', views.tendencias_comparativas, name='TendenciasComparativas'),
    path('logout/', LogoutView.as_view(next_page='/login/auth0'), name='logout'),
]
