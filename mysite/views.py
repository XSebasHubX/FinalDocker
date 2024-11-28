"""xxxxxxxx."""
import json
from decouple import config
from django.contrib.auth import logout as django_logout
from django.http import HttpResponseRedirect
from django.shortcuts import render
import pandas as pd
from django.http import JsonResponse
import os
from django.conf import settings
import plotly.express as px
import plotly.graph_objects as go
from django.views.decorators.clickjacking import xframe_options_exempt
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import logout
from django.shortcuts import redirect



def index(request):
    """xxxxxxxxx"""
    return render(request,'index.html')


def inicio(request):
    """xxxxxxxxx"""
    return render(request,'portada.html')

def inventario(request):
    """xxxxxxxxx"""
    # Leer el archivo Excel
    df = pd.read_excel('DataSet-AdidasSale.xlsx')
    
    # Calcular estadísticas
    total_ventas = f"${df['TotalSales'].sum():,.2f}"
    total_unidades = f"{df['UnitsSold'].sum():,}"
    promedio_precio = f"${df['PricePerUnit'].mean():.2f}"
    
    # Crear gráfico de ventas por producto
    fig_ventas = px.bar(
        df.groupby('Product')['TotalSales'].sum().reset_index(),
        x='Product',
        y='TotalSales',
        title='Ventas por Producto'
    )
    grafico_ventas = fig_ventas.to_html(full_html=False)
    
    # Crear gráfico de ventas por región
    fig_region = px.pie(
        df.groupby('Region')['TotalSales'].sum().reset_index(),
        values='TotalSales',
        names='Region',
        title='Ventas por Región'
    )
    grafico_region = fig_region.to_html(full_html=False)
    
    # Preparar datos para la tabla
    datos_tabla = df.to_dict('records')
    
    context = {
        'total_ventas': total_ventas,
        'total_unidades': total_unidades,
        'promedio_precio': promedio_precio,
        'grafico_ventas': grafico_ventas,
        'grafico_region': grafico_region,
        'datos_tabla': datos_tabla,
    }
    
    return render(request, 'Inventario.html', context)

def profile(request):
    """xxxxxxxxx"""
    user=request.user

    auth0_user=user.social_auth.get(provider='auth0')

    user_data={
        'user_id':auth0_user.uid,
        'name':user.first_name,
        'picture':auth0_user.extra_data['picture']

    }

    context={
        'user_data':json.dumps(user_data,indent=4),
        'auth0_user':auth0_user
    }

    return render(request, 'profile.html', context)
#logout
#https://{domain}/v2/logout?client_id={client_id}&returnTo={return_to}

def logout(request):
    """xxxxxxxxx"""
    django_logout(request)

    domain=config('APP_DOMAIN')
    client_id=config('APP_CLIENT_ID')
    return_to='http://127.0.0.1:8000'

    logout_url = f"https://{domain}/v2/logout?client_id={client_id}&returnTo={return_to}"

    return HttpResponseRedirect(logout_url)

def inventario_view(request):
    try:
        # Ruta al archivo Excel
        excel_path = os.path.join(settings.BASE_DIR, 'data', 'DataSet-AdidasSale.xlsx')
        
        # Lee el archivo Excel
        df = pd.read_excel(excel_path)
        print(f"DataFrame cargado con {len(df)} filas")
        print("Columnas:", df.columns.tolist())
        
        # Prepara datos para las gráficas
        # Top 10 productos por unidades vendidas
        product_sales = df.groupby('Product')['UnitsSold'].sum().nlargest(10).to_dict()
        
        # Ventas por región
        sales_by_region = df.groupby('Region')['TotalSales'].sum().round(2).to_dict()
        
        # Precio promedio por producto (top 10)
        avg_price_by_product = df.groupby('Product')['PricePerUnit'].mean().nlargest(10).round(2).to_dict()
        
        # Ventas por método
        sales_by_method = df.groupby('SalesMethod')['TotalSales'].sum().round(2).to_dict()
        
        # Prepara datos para la tabla
        datos_adidas = df.to_dict('records')
        
        context = {
            'datos_adidas': datos_adidas,
            'chart_data': {
                'product_sales': product_sales,
                'sales_by_region': sales_by_region,
                'avg_price_by_product': avg_price_by_product,
                'sales_by_method': sales_by_method
            }
        }
        
        return render(request, 'Inventario.html', context)
        
    except Exception as e:
        print(f"Error al cargar los datos: {str(e)}")
        return render(request, 'Inventario.html', {
            'error_message': str(e),
            'datos_adidas': [],
            'chart_data': {
                'product_sales': {},
                'sales_by_region': {},
                'avg_price_by_product': {},
                'sales_by_method': {}
            }
        })

@xframe_options_exempt
@csrf_exempt
def tu_vista(request):
    # tu código aquí
    return render(request, 'tu_template.html')

def custom_logout(request):
    logout(request)
    return redirect('portada')
