import os
import plotly.express as px
from plotly.offline import plot
import pandas as pd
import plotly.graph_objects as go
import pandas as pd
from django.shortcuts import render
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from django.contrib.auth import logout
from django.shortcuts import redirect
from django.conf import settings
from urllib.parse import quote_plus
from django.urls import reverse

def ventas_dashboard(request):
    df = pd.read_excel("data/DataSet-AdidasSale.xlsx")
    df.dropna(subset=['Retailer', 'RetailerID', 'InvoiceDate', 'Region', 'State', 'City','Product','PricePerUnit','UnitsSold','TotalSales', 'OperatingProfit', 'OperatingMargin', 'SalesMethod'], inplace=True)

    # Ventas totales, unidades totales vendidas y utilidad operativa total
    ventas_totales = round(df['TotalSales'].sum(), 0)
    unidades_totales_vendidas = round(df['UnitsSold'].sum(), 0)
    utilidad_operativa_total = round(df['OperatingProfit'].sum(), 2)

    # Comparación de ventas totales por minorista
    comparacion_ventas_minoristas = df.groupby('Retailer')['TotalSales'].sum().reset_index().rename(columns={'TotalSales': 'Ventas_Totales'})
    
    # Distribución de ventas por mes - Modificación
    df['InvoiceDate'] = pd.to_datetime(df['InvoiceDate'], errors='coerce')
    df.dropna(subset=['InvoiceDate'], inplace=True)
    df['Mes'] = df['InvoiceDate'].dt.strftime('%Y-%m')  # Cambiado el formato del mes
    
    resumen_ventas_beneficio_mes = df.groupby('Mes').agg({
        'TotalSales': 'sum',
        'OperatingProfit': 'sum'
    }).reset_index()
    
    # Asegúrate de que estas líneas estén antes de crear la gráfica
    df['InvoiceDate'] = pd.to_datetime(df['InvoiceDate'])
    ventas_mensuales = df.groupby(df['InvoiceDate'].dt.strftime('%Y-%m')).agg({
        'TotalSales': 'sum',
        'OperatingProfit': 'sum'
    }).reset_index()

    # Crear la gráfica
    fig = go.Figure()

    # Agregar barras para ventas
    fig.add_trace(go.Bar(
        x=ventas_mensuales['InvoiceDate'],
        y=ventas_mensuales['TotalSales'],
        name='Ventas',
        marker_color='#000000'
    ))

    # Agregar línea para beneficios
    fig.add_trace(go.Scatter(
        x=ventas_mensuales['InvoiceDate'],
        y=ventas_mensuales['OperatingProfit'],
        name='Beneficios',
        line=dict(color='#FF0000', width=2),
        mode='lines+markers'
    ))

    # Actualizar el diseño
    fig.update_layout(
        title='Distribución Mensual de Ventas y Beneficios',
        xaxis_title='Mes',
        yaxis_title='Cantidad ($)',
        template='plotly_white',
        height=400,
        showlegend=True
    )

    # Convertir a HTML
    grafica_distribucion_mensual = fig.to_html(
        full_html=False,
        include_plotlyjs=True,
        config={'displayModeBar': False}
    )

    # Ventas totales por región
    resumen_ventas_region = df.groupby('Region')['TotalSales'].sum().reset_index().rename(columns={'TotalSales': 'Ventas_Totales'})
    
    context = {
        'resumen_ventas_region': resumen_ventas_region.to_dict('records'),
        'resumen_ventas_beneficio_mes': resumen_ventas_beneficio_mes.to_dict('records'),
        'comparacion_ventas_minoristas': comparacion_ventas_minoristas.to_dict('records'),
        'ventas_totales': ventas_totales,
        'unidades_totales_vendidas': unidades_totales_vendidas,
        'utilidad_operativa_total': utilidad_operativa_total,
        'usuario_actual': request.user,
        'grafica_distribucion_mensual': grafica_distribucion_mensual,
    }

    return render(request, 'data_analisys/dashboard.html',context)

# ------------------------------------------------------------------------------------------------------------------------------------------

def analisis_regional(request):
    df = pd.read_excel("data/DataSet-AdidasSale.xlsx")
    df.dropna(subset=['Region', 'State', 'TotalSales', 'OperatingProfit', 'InvoiceDate'], inplace=True)
    
    # Configuración común
    config = {
        'displayModeBar': False,
        'responsive': True,
        'scrollZoom': False,
        'showLink': False,
        'displaylogo': False,
        'modeBarButtonsToRemove': ['zoom', 'pan', 'select', 'lasso2d']
    }

    # Tema personalizado
    tema_personalizado = {
        'paper_bgcolor': '#FFFFFF',
        'plot_bgcolor': '#FFFFFF',
        'font': {
            'family': 'AdihausDIN, Arial, sans-serif',
            'color': '#000000'
        },
        'colorway': ['#0066B2', '#FF0000', '#000000', '#209CE8', '#FF385C', '#343A40'],
        'margin': dict(l=20, r=20, t=70, b=20)
    }

    # Preparación de datos
    df['InvoiceDate'] = pd.to_datetime(df['InvoiceDate'])
    fecha_maxima = df['InvoiceDate'].max()
    
    periodo = request.GET.get('periodo', 'year')
    
    if periodo == 'month':
        df_filtrado = df[df['InvoiceDate'] >= fecha_maxima - pd.DateOffset(months=1)]
        periodo_texto = "Último Mes"
    elif periodo == 'quarter':
        df_filtrado = df[df['InvoiceDate'] >= fecha_maxima - pd.DateOffset(months=3)]
        periodo_texto = "Último Trimestre"
    else:
        df_filtrado = df[df['InvoiceDate'] >= fecha_maxima - pd.DateOffset(years=1)]
        periodo_texto = "Último Año"

    # Gráfico 1: Pastel de distribución de ventas
    resumen_region = df_filtrado.groupby('Region')['TotalSales'].sum().reset_index()
    grafico_pastel = go.Figure(data=[
        go.Pie(
            labels=resumen_region['Region'],
            values=resumen_region['TotalSales'],
            hole=0.5,
            textinfo='label+percent',
            textposition='outside',
            marker=dict(colors=tema_personalizado['colorway']),
            pull=[0.1 if i == 0 else 0 for i in range(len(resumen_region))],
            rotation=90,
            direction='clockwise'
        )
    ])

    grafico_pastel.update_layout(
        **tema_personalizado,
        title=dict(
            text='Distribución de Ventas por Región',
            x=0.5,
            y=0.95,
            xanchor='center',
            yanchor='top',
            font=dict(size=24)
        ),
        annotations=[dict(
            text=f'Total<br>${resumen_region["TotalSales"].sum():,.0f}',
            x=0.5,
            y=0.5,
            font=dict(size=20),
            showarrow=False
        )],
        height=500
    )

    # Gráfico 2: Barras apiladas de ventas por estado
    resumen_ventas_region = df_filtrado.groupby(['Region', 'State'])['TotalSales'].sum().reset_index()
    grafico_barras_apiladas = go.Figure()
    
    for state in df_filtrado['State'].unique():
        state_data = resumen_ventas_region[resumen_ventas_region['State'] == state]
        grafico_barras_apiladas.add_trace(
            go.Bar(
                name=state,
                x=state_data['Region'],
                y=state_data['TotalSales'],
                text=state_data['TotalSales'].apply(lambda x: f'${x:,.0f}'),
                textposition='auto'
            )
        )

    grafico_barras_apiladas.update_layout(
        **tema_personalizado,
        title=dict(
            text='Ventas por Región y Estado',
            x=0.5,
            y=0.95,
            xanchor='center',
            yanchor='top',
            font=dict(size=24)
        ),
        barmode='stack',
        height=600
    )

    # Gráfico 3: Barras de beneficio operativo
    resumen_beneficio = df_filtrado.groupby('Region')['OperatingProfit'].sum().reset_index()
    grafico_barras = go.Figure(data=[
        go.Bar(
            x=resumen_beneficio['Region'],
            y=resumen_beneficio['OperatingProfit'],
            text=resumen_beneficio['OperatingProfit'].apply(lambda x: f'${x:,.0f}'),
            textposition='auto',
            marker_color=tema_personalizado['colorway'][2]
        )
    ])

    grafico_barras.update_layout(
        **tema_personalizado,
        title=dict(
            text='Beneficio Operativo por Región',
            x=0.5,
            y=0.95,
            xanchor='center',
            yanchor='top',
            font=dict(size=24)
        ),
        height=500,
        yaxis=dict(
            title='Beneficio Operativo ($)',
            tickformat='$,.0f'
        )
    )

    # Convertir gráficos a HTML
    pastel_html = grafico_pastel.to_html(full_html=False, config=config)
    barras_apiladas_html = grafico_barras_apiladas.to_html(full_html=False, config=config)
    barras_html = grafico_barras.to_html(full_html=False, config=config)

    context = {
        'grafico_pastel': pastel_html,
        'grafico_barras_apiladas': barras_apiladas_html,
        'grafico_barras': barras_html,
        'periodo_actual': periodo,
        'periodo_texto': periodo_texto
    }

    return render(request, 'data_analisys/AnalisisRegional.html', context)

def desempeno_producto(request):
    df = pd.read_excel("data/DataSet-AdidasSale.xlsx")
    df.dropna(subset=['Product', 'PricePerUnit', 'UnitsSold', 'TotalSales', 'Region'], inplace=True)

    # Configuración del tema personalizado
    tema_personalizado = {
        'paper_bgcolor': '#FFFFFF',
        'plot_bgcolor': '#FFFFFF',
        'font': {
            'family': 'AdihausDIN, Arial, sans-serif',
            'color': '#000000'
        },
        'colorway': ['#0066B2', '#FF0000', '#000000', '#209CE8', '#FF385C', '#343A40']
    }

    # Configuración de animación para las gráficas
    animation_settings = dict(
        frame=dict(duration=1000, redraw=True),
        transition=dict(duration=500, easing="cubic-in-out")
    )

    # 1. Gráfica de barras con animación
    ventas_por_producto = df.groupby('Product')['UnitsSold'].sum().reset_index()
    ventas_por_producto = ventas_por_producto.sort_values(by='UnitsSold', ascending=True).tail(10)
    
    grafico_barras = go.Figure(data=[
        go.Bar(
            y=ventas_por_producto['Product'],
            x=ventas_por_producto['UnitsSold'],
            orientation='h',
            marker=dict(
                color=tema_personalizado['colorway'][0],
                line=dict(color='#000000', width=1)
            ),
            text=ventas_por_producto['UnitsSold'].map('{:,.0f}'.format),
            textposition='auto',
        )
    ])

    grafico_barras.update_layout(
        **tema_personalizado,
        title_text='Top 10 Productos más Vendidos',
        title_x=0.5,
        title_y=0.95,
        title_xanchor='center',
        title_yanchor='top',
        xaxis_title='Unidades Vendidas',
        yaxis_title=None,
        showlegend=False,
        height=500,
        margin=dict(l=20, r=20, t=70, b=20),
        # Configuración de animación
        updatemenus=[dict(
            type='buttons',
            showactive=False,
            y=1.1,
            x=0.1,
            xanchor='right',
            yanchor='top',
            buttons=[dict(
                label='Reproducir',
                method='animate',
                args=[None, dict(
                    frame=dict(duration=500, redraw=True),
                    fromcurrent=True,
                    transition=dict(
                        duration=300,
                        easing='quadratic-in-out'
                    )
                )]
            )]
        )],
        # Frames para la animación
        sliders=[dict(
            currentvalue=dict(
                font=dict(size=12),
                prefix='Velocidad: ',
                visible=True,
                xanchor='right'
            )
        )]
    )

    # Crear frames para la animación
    frames = [
        go.Frame(
            data=[go.Bar(
                x=[val * (k/20) for val in ventas_por_producto['UnitsSold']],
                y=ventas_por_producto['Product'],
                orientation='h',
                marker=dict(
                    color=tema_personalizado['colorway'][0],
                    line=dict(color='#000000', width=1)
                ),
                text=ventas_por_producto['UnitsSold'].map('{:,.0f}'.format),
                textposition='auto',
            )],
            name=f'frame{k}'
        )
        for k in range(21)
    ]

    grafico_barras.frames = frames

    # 2. Gráfica de pastel con animación
    ventas_por_producto = df.groupby('Product')['TotalSales'].sum().reset_index()
    ventas_por_producto = ventas_por_producto.sort_values(by='TotalSales', ascending=True).tail(8)
    
    grafico_pastel = go.Figure(data=[
        go.Pie(
            labels=ventas_por_producto['Product'],
            values=ventas_por_producto['TotalSales'],
            hole=0.5,
            textinfo='label+percent',
            textposition='outside',
            marker=dict(colors=tema_personalizado['colorway']),
            pull=[0.1 if i == 0 else 0 for i in range(len(ventas_por_producto))],
            rotation=90,
            direction='clockwise'
        )
    ])

    grafico_pastel.update_layout(
        **tema_personalizado,
        title_text='Distribución de Ventas por Producto',
        title_x=0.5,
        title_y=0.95,
        title_xanchor='center',
        title_yanchor='top',
        annotations=[dict(
            text=f'Total<br>${ventas_por_producto["TotalSales"].sum():,.0f}',
            x=0.5,
            y=0.5,
            font=dict(size=20),
            showarrow=False
        )],
        height=500,
        margin=dict(l=20, r=20, t=70, b=20),
        # Configuración de animación
        updatemenus=[dict(
            type='buttons',
            showactive=False,
            x=0.1,
            y=1.1,
            xanchor='right',
            yanchor='top',
            buttons=[dict(
                label='Girar',
                method='animate',
                args=[None, dict(
                    frame=dict(duration=1000, redraw=True),
                    fromcurrent=True,
                    transition=dict(
                        duration=500,
                        easing='cubic-in-out'
                    )
                )]
            )]
        )]
    )

    # Crear frames para la animación del gráfico de pastel
    frames_pastel = [
        go.Frame(
            data=[go.Pie(
                labels=ventas_por_producto['Product'],
                values=ventas_por_producto['TotalSales'],
                hole=0.5,
                textinfo='label+percent',
                textposition='outside',
                marker=dict(colors=tema_personalizado['colorway']),
                pull=[0.1 if i == 0 else 0 for i in range(len(ventas_por_producto))],
                rotation=90 + (i * 360/20),  # Rotación gradual
                direction='clockwise'
            )],
            name=f'frame{i}'
        )
        for i in range(20)
    ]

    grafico_pastel.frames = frames_pastel

    # 3. Relación precio-unidades (Gráfica mejorada)
    grafico_burbuja = go.Figure()

    # Crear una escala de colores personalizada para Adidas
    colores_adidas = [
        [0, '#0066B2'],      # Azul Adidas
        [0.33, '#FF0000'],   # Rojo Adidas
        [0.66, '#000000'],   # Negro Adidas
        [1, '#209CE8']       # Azul claro
    ]

    # Calcular el tamaño de las burbujas de manera más proporcional
    max_ventas = df['TotalSales'].max()
    tamano_burbujas = df['TotalSales'] / max_ventas * 50  # Ajusta el 50 según necesites

    for idx, region in enumerate(df['Region'].unique()):
        df_region = df[df['Region'] == region]
        
        grafico_burbuja.add_trace(
            go.Scatter(
                x=df_region['PricePerUnit'],
                y=df_region['UnitsSold'],
                mode='markers',
                name=region,
                marker=dict(
                    size=df_region['TotalSales'] / max_ventas * 50,
                    sizemode='area',
                    sizeref=2. * max(tamano_burbujas) / (40.**2),
                    sizemin=4,
                    color=df_region['TotalSales'],
                    colorscale=colores_adidas,
                    showscale=True if idx == 0 else False,
                    colorbar=dict(
                        title="Ventas Totales ($)",
                        tickprefix="$",
                        tickformat=",.0f",
                        len=0.8,
                        thickness=15,
                        outlinewidth=0,
                        bgcolor='rgba(255,255,255,0.8)'
                    ),
                    opacity=0.8,
                    line=dict(
                        color='white',
                        width=1
                    )
                ),
                hovertemplate=(
                    "<b>%{text}</b><br>" +
                    "Región: " + region + "<br>" +
                    "Precio: $%{x:,.2f}<br>" +
                    "Unidades: %{y:,.0f}<br>" +
                    "Ventas: $%{customdata:,.2f}<br>" +
                    "<extra></extra>"
                ),
                text=df_region['Product'],
                customdata=df_region['TotalSales']
            )
        )

    grafico_burbuja.update_layout(
        **tema_personalizado,
        title_text='Análisis de Precio vs. Demanda por Región',
        title_x=0.5,
        title_y=0.95,
        title_xanchor='center',
        title_yanchor='top',
        xaxis=dict(
            title='Precio por Unidad ($)',
            tickprefix='$',
            gridcolor='rgba(0,0,0,0.1)',
            zerolinecolor='rgba(0,0,0,0.2)',
            showgrid=True
        ),
        yaxis=dict(
            title='Unidades Vendidas',
            tickformat=',d',
            gridcolor='rgba(0,0,0,0.1)',
            zerolinecolor='rgba(0,0,0,0.2)',
            showgrid=True
        ),
        height=700,
        showlegend=True,
        legend=dict(
            yanchor="top",
            y=0.99,
            xanchor="left",
            x=0.01,
            bgcolor='rgba(255,255,255,0.8)',
            bordercolor='rgba(0,0,0,0.1)',
            borderwidth=1
        ),
        margin=dict(l=20, r=20, t=70, b=20),
        shapes=[
            dict(
                type='line',
                x0=df['PricePerUnit'].min(),
                x1=df['PricePerUnit'].max(),
                y0=df['UnitsSold'].mean(),
                y1=df['UnitsSold'].mean(),
                line=dict(
                    color='rgba(0,0,0,0.1)',
                    dash='dash'
                )
            )
        ],
        annotations=[
            dict(
                text='Tamaño de burbuja = Ventas Totales',
                x=0.02,
                y=1.05,
                xref='paper',
                yref='paper',
                showarrow=False,
                font=dict(size=10, color='gray')
            )
        ],
        updatemenus=[dict(
            type='buttons',
            showactive=False,
            buttons=[dict(
                label="Animar",
                method="animate",
                args=[None, dict(
                    frame=dict(duration=1000, redraw=True),
                    transition=dict(duration=500, easing="cubic-in-out"),
                    fromcurrent=True,
                    mode='immediate'
                )]
            )]
        )]
    )

    # Agregar rangos y líneas de referencia
    grafico_burbuja.add_hline(
        y=df['UnitsSold'].median(),
        line_dash="dot",
        line_color="rgba(0,0,0,0.2)",
        annotation_text="Mediana de Unidades"
    )

    grafico_burbuja.add_vline(
        x=df['PricePerUnit'].median(),
        line_dash="dot",
        line_color="rgba(0,0,0,0.2)",
        annotation_text="Mediana de Precio"
    )

    # Configuración adicional para animaciones en el HTML
    config = {
        'displayModeBar': False,
        'responsive': True,
        'scrollZoom': False,
        'showLink': False,
        'displaylogo': False,
        'modeBarButtonsToRemove': ['zoom', 'pan', 'select', 'lasso2d']
    }

    # Convertir gráficos a HTML con animaciones
    barras_html = grafico_barras.to_html(full_html=False, config=config, include_plotlyjs=True)
    pastel_html = grafico_pastel.to_html(full_html=False, config=config, include_plotlyjs=True)
    burbuja_html = grafico_burbuja.to_html(full_html=False, config=config, include_plotlyjs=True)

    context = {
        'grafico_barras': barras_html,
        'grafico_pastel': pastel_html,
        'grafico_burbuja': burbuja_html,
    }

    return render(request, 'data_analisys/DesempeñoProducto.html', context)


def tendencias_comparativas(request):
    df = pd.read_excel("data/DataSet-AdidasSale.xlsx")
    df.dropna(subset=['Retailer', 'RetailerID', 'InvoiceDate', 'Region', 'State', 'City',
                    'Product', 'PricePerUnit', 'UnitsSold', 'TotalSales',
                    'OperatingProfit', 'OperatingMargin', 'SalesMethod'], inplace=True)

    # Tema personalizado de Adidas
    tema_personalizado = {
        'template': 'plotly_white',
        'paper_bgcolor': 'white',
        'plot_bgcolor': 'white',
        'font': {
            'family': 'AdihausDIN, Arial, sans-serif',
            'color': '#000000'
        },
        'margin': dict(t=100, l=80, r=80, b=80),
        'showlegend': True,
        'legend': {
            'bgcolor': 'rgba(255, 255, 255, 0.9)',
            'bordercolor': '#E9ECEF',
            'borderwidth': 1
        }
    }

    # Colores corporativos de Adidas
    colores_adidas = ['#0066B2', '#FF0000', '#000000', '#209CE8', '#FF385C']

    # 1. Gráfico de BoxPlot con animación mejorada
    df['RangoVentas'] = pd.qcut(df['TotalSales'], q=4, labels=['Bajas', 'Medias-Bajas', 'Medias-Altas', 'Altas'])
    grafico_boxplot = go.Figure()
    
    # Crear frames para la animación del BoxPlot
    frames_boxplot = []
    rangos = df['RangoVentas'].unique()
    
    # Frame inicial (todos ocultos)
    for i, rango in enumerate(rangos):
        datos_rango = df[df['RangoVentas'] == rango]['OperatingMargin']
        grafico_boxplot.add_trace(go.Box(
            y=datos_rango,
            name=rango,
            marker_color=colores_adidas[i],
            boxpoints='outliers',
            marker=dict(
                opacity=0,
                size=4,
                color=colores_adidas[i]
            ),
            line=dict(width=2),
            opacity=0
        ))

    # Crear frames para la animación
    for step in range(6):  # 6 pasos de animación
        frame_data = []
        for i, rango in enumerate(rangos):
            datos_rango = df[df['RangoVentas'] == rango]['OperatingMargin']
            
            # Calcular la opacidad y el tamaño basado en el paso
            opacity = min(1, step/4)
            marker_size = min(4, step * 1)
            
            frame_data.append(go.Box(
                y=datos_rango,
                name=rango,
                marker_color=colores_adidas[i],
                boxpoints='outliers',
                marker=dict(
                    opacity=opacity,
                    size=marker_size,
                    color=colores_adidas[i]
                ),
                line=dict(width=2),
                opacity=opacity,
                # Añadir efecto de "bounce"
                offsetgroup=str(i),
                jitter=0.3,
                pointpos=(-1.8 + step/2) if step < 4 else -0.3
            ))
        frames_boxplot.append(go.Frame(
            data=frame_data,
            name=f'frame{step}',
            traces=[0,1,2,3]
        ))

    grafico_boxplot.frames = frames_boxplot

    # Actualizar el layout con animación mejorada
    grafico_boxplot.update_layout(
        **tema_personalizado,
        title=dict(
            text='Relación entre Margen Operativo y Total de Ventas',
            font=dict(size=24, color='#000000'),
            x=0.5,
            xanchor='center'
        ),
        yaxis=dict(
            title='Margen Operativo (%)',
            gridcolor='#E9ECEF',
            zeroline=True,
            zerolinecolor='#000000',
            zerolinewidth=1
        ),
        xaxis=dict(
            title='Rango de Ventas',
            gridcolor='#E9ECEF'
        ),
        boxmode='group',
        height=600,
        # Configuración de animación mejorada
        updatemenus=[
            {
                'buttons': [
                    {
                        'args': [None, {
                            'frame': {'duration': 500, 'redraw': True},
                            'fromcurrent': True,
                            'transition': {
                                'duration': 300,
                                'easing': 'cubic-in-out'
                            }
                        }],
                        'label': 'Reproducir',
                        'method': 'animate'
                    },
                    {
                        'args': [[None], {
                            'frame': {'duration': 0, 'redraw': True},
                            'mode': 'immediate',
                            'transition': {'duration': 0}
                        }],
                        'label': 'Pausar',
                        'method': 'animate'
                    }
                ],
                'direction': 'left',
                'pad': {'r': 10, 't': 87},
                'showactive': False,
                'type': 'buttons',
                'x': 0.1,
                'xanchor': 'right',
                'y': 0,
                'yanchor': 'top'
            }
        ],
        # Agregar slider para control manual de la animación
        sliders=[{
            'active': 0,
            'yanchor': 'top',
            'xanchor': 'left',
            'currentvalue': {
                'font': {'size': 16},
                'prefix': 'Paso: ',
                'visible': True,
                'xanchor': 'right'
            },
            'transition': {'duration': 300, 'easing': 'cubic-in-out'},
            'pad': {'b': 10, 't': 50},
            'len': 0.9,
            'x': 0.1,
            'y': 0,
            'steps': [
                {
                    'args': [
                        [f'frame{k}'],
                        {'frame': {'duration': 300, 'redraw': True},
                         'mode': 'immediate',
                         'transition': {'duration': 300}}
                    ],
                    'label': str(k + 1),
                    'method': 'animate'
                } for k in range(6)
            ]
        }],
        # Añadir efectos visuales adicionales
        shapes=[
            # Línea de referencia
            dict(
                type='line',
                xref='paper',
                yref='y',
                x0=0,
                y0=df['OperatingMargin'].mean(),
                x1=1,
                y1=df['OperatingMargin'].mean(),
                line=dict(
                    color='rgba(0,0,0,0.2)',
                    width=1,
                    dash='dash'
                )
            )
        ]
    )

    # 2. Gráfico de Líneas con animación
    df['InvoiceDate'] = pd.to_datetime(df['InvoiceDate'], errors='coerce')
    df['Mes'] = df['InvoiceDate'].dt.to_period('M').astype(str)
    resumen_margen = df.groupby('Mes').agg({
        'OperatingMargin': ['mean', 'std']
    }).reset_index()
    resumen_margen.columns = ['Mes', 'Margen_Promedio', 'Margen_Std']

    grafico_lineas = go.Figure()

    # Crear frames para la animación de líneas
    frames_lineas = []
    for i in range(len(resumen_margen)):
        frame_data = [
            # Banda superior
            go.Scatter(
                x=resumen_margen['Mes'][:i+1],
                y=resumen_margen['Margen_Promedio'][:i+1] + resumen_margen['Margen_Std'][:i+1],
                fill=None,
                mode='lines',
                line_color='rgba(0, 102, 178, 0.1)',
                showlegend=False
            ),
            # Banda inferior
            go.Scatter(
                x=resumen_margen['Mes'][:i+1],
                y=resumen_margen['Margen_Promedio'][:i+1] - resumen_margen['Margen_Std'][:i+1],
                fill='tonexty',
                mode='lines',
                line_color='rgba(0, 102, 178, 0.1)',
                showlegend=False
            ),
            # Línea principal
            go.Scatter(
                x=resumen_margen['Mes'][:i+1],
                y=resumen_margen['Margen_Promedio'][:i+1],
                mode='lines+markers',
                name='Margen Operativo',
                line=dict(color=colores_adidas[0], width=3),
                marker=dict(size=8, symbol='circle')
            )
        ]
        frames_lineas.append(go.Frame(data=frame_data, name=f'frame{i}'))

    # Añadir datos iniciales
    grafico_lineas.add_traces([frames_lineas[0].data[0], frames_lineas[0].data[1], frames_lineas[0].data[2]])
    grafico_lineas.frames = frames_lineas

    grafico_lineas.update_layout(
        **tema_personalizado,
        title=dict(
            text='Evolución del Margen Operativo Mensual',
            font=dict(size=24, color='#000000'),
            x=0.5,
            xanchor='center'
        ),
        xaxis=dict(
            title='Mes',
            gridcolor='#E9ECEF',
            tickangle=45
        ),
        yaxis=dict(
            title='Margen Operativo (%)',
            gridcolor='#E9ECEF',
            zeroline=True,
            zerolinecolor='#000000',
            zerolinewidth=1
        ),
        height=600,
        # Configuración de animación
        updatemenus=[dict(
            type='buttons',
            showactive=False,
            buttons=[dict(
                label='Reproducir',
                method='animate',
                args=[None, dict(
                    frame=dict(duration=100, redraw=True),
                    fromcurrent=True,
                    transition=dict(duration=50)
                )]
            )]
        )]
    )

    # 3. Gráfico de Barras con animación
    ventas_por_metodo = df.groupby('SalesMethod').agg({
        'TotalSales': 'sum',
        'OperatingProfit': 'sum'
    }).reset_index()

    grafico_barras = go.Figure()

    # Crear frames para la animación de barras
    frames_barras = []
    for i in range(21):  # 20 pasos de animación
        frame_data = [
            go.Bar(
                x=ventas_por_metodo['SalesMethod'],
                y=ventas_por_metodo['TotalSales'] * (i/20),
                name='Ventas Totales',
                marker_color=colores_adidas[0],
                text=(ventas_por_metodo['TotalSales'] * (i/20)).apply(lambda x: f'${x:,.0f}'),
                textposition='auto',
            ),
            go.Bar(
                x=ventas_por_metodo['SalesMethod'],
                y=ventas_por_metodo['OperatingProfit'] * (i/20),
                name='Beneficio Operativo',
                marker_color=colores_adidas[1],
                text=(ventas_por_metodo['OperatingProfit'] * (i/20)).apply(lambda x: f'${x:,.0f}'),
                textposition='auto',
            )
        ]
        frames_barras.append(go.Frame(data=frame_data, name=f'frame{i}'))

    # Añadir datos iniciales
    grafico_barras.add_traces([frames_barras[0].data[0], frames_barras[0].data[1]])
    grafico_barras.frames = frames_barras

    grafico_barras.update_layout(
        **tema_personalizado,
        title=dict(
            text='Comparativa de Ventas y Beneficios por Método de Venta',
            font=dict(size=24, color='#000000'),
            x=0.5,
            xanchor='center'
        ),
        barmode='group',
        xaxis=dict(
            title='Método de Venta',
            gridcolor='#E9ECEF'
        ),
        yaxis=dict(
            title='Monto ($)',
            gridcolor='#E9ECEF',
            tickformat='$,.0f'
        ),
        height=600,
        # Configuración de animación
        updatemenus=[dict(
            type='buttons',
            showactive=False,
            buttons=[dict(
                label='Reproducir',
                method='animate',
                args=[None, dict(
                    frame=dict(duration=50, redraw=True),
                    fromcurrent=True,
                    transition=dict(duration=50)
                )]
            )]
        )]
    )

    # Configuración mejorada para la exportación HTML
    config = {
        'displayModeBar': True,
        'displaylogo': False,
        'modeBarButtonsToRemove': ['lasso2d', 'select2d'],
        'responsive': True,
        'scrollZoom': True
    }

    boxplot_html = grafico_boxplot.to_html(full_html=False, config=config)
    lineas_html = grafico_lineas.to_html(full_html=False, config=config)
    barras_html = grafico_barras.to_html(full_html=False, config=config)

    context = {
        'grafico_boxplot': boxplot_html,
        'grafico_lineas': lineas_html,
        'grafico_barras': barras_html,
    }

    return render(request, 'data_analisys/TendenciasComparativas.html', context)

def inventario_view(request):
    try:
        # Lee el archivo Excel
        df = pd.read_excel("data/DataSet-AdidasSale.xlsx")
        df.dropna(subset=['Retailer', 'RetailerID', 'InvoiceDate', 'Region', 'State', 'City',
                         'Product', 'PricePerUnit', 'UnitsSold', 'TotalSales',
                         'OperatingProfit', 'OperatingMargin', 'SalesMethod'], inplace=True)

        # Prepara datos para las gráficas
        # Top 10 productos por ventas
        product_sales = df.groupby('Product')['TotalSales'].sum().nlargest(10).round(2).to_dict()
        
        # Ventas por región
        sales_by_region = df.groupby('Region')['TotalSales'].sum().round(2).to_dict()
        
        # Precio promedio por producto (top 10)
        avg_price_by_product = df.groupby('Product')['PricePerUnit'].mean().nlargest(10).round(2).to_dict()
        
        # Ventas por método
        sales_by_method = df.groupby('SalesMethod')['TotalSales'].sum().round(2).to_dict()

        # Prepara datos para la tabla
        datos_adidas = df.to_dict('records')
        
        context = {
            'datos_adidas': datos_adidas[:50],  # Limitamos a 50 registros para la tabla
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

def logout_view(request):
    """
    Vista para manejar el cierre de sesión.
    """
    # Primero hacemos logout en Django
    logout(request)   