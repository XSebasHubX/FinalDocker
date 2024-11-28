# FinalDocker
proyecto final herrmaientas de programacion y topicos 1
Django con Docker - Aplicación Web con Autenticación y Dashboard
Este proyecto es una aplicación web basada en Django, diseñada para ejecutarse dentro de un entorno Dockerizado. Incluye funcionalidades de autenticación mediante Auth0, análisis de datos con Pandas, y un dashboard interactivo para visualizar métricas con librerías como Plotly o Chart.js.

Características Principales
Autenticación y autorización: Implementación con Auth0, roles de usuario (Usuario y Administrador) y permisos diferenciados.
Análisis de datos: Procesamiento de datos utilizando Pandas, con generación de métricas y resultados visualizados en gráficos.
Dashboard interactivo: Visualización de datos en tiempo real a través de gráficos dinámicos.
Dockerización: Despliegue de la aplicación Django y la base de datos SQLite mediante contenedores Docker.
Estructura modular: Organización del código en componentes separados para facilitar el desarrollo y mantenimiento.
Estructura del Proyecto
plaintext
Copiar código
docker-django/  
 Dockerfile               # Construcción de la imagen Docker de Django.  
 docker-compose.yml       # Orquestación de servicios Docker.  
 manage.py                # Herramienta para administración del proyecto Django.  
 db.sqlite3               # Base de datos SQLite.  
 requirements.txt         # Dependencias del proyecto.  
 config/                  # Configuración global de Django.  
 data/                    # Directorio para datos utilizados en el análisis.  
 data_analisys/           # Scripts y herramientas de análisis de datos.  
 mysite/                  # Código fuente de la aplicación Django.  
 static/                  # Archivos estáticos de la aplicación.  
 venv/                    # Entorno virtual Python (opcional si se usa Docker).  
Instalación
Requisitos Previos
Docker y Docker Compose instalados.
Python 3.8+ (opcional, solo para configuraciones fuera de Docker).
Cuenta Auth0 para configuración de autenticación.
Configuración Inicial
Clonar el repositorio

bash
Copiar código
git clone <URL-del-repositorio>  
cd docker-django  
Crear archivo .env
Genera un archivo .env con las siguientes variables:

env
Copiar código
SECRET_KEY=<clave_secreta_django>  
DEBUG=True  
AUTH0_DOMAIN=<tu_dominio_auth0>  
AUTH0_CLIENT_ID=<tu_client_id_auth0>  
AUTH0_CLIENT_SECRET=<tu_client_secret_auth0>  
Iniciar contenedores Docker
Construye y ejecuta los servicios con:

bash
Copiar código
docker-compose up --build  
Uso
Accede a la aplicación en: http://localhost:8000.
Inicia sesión con una cuenta configurada en Auth0.
Explora el dashboard y visualiza métricas o gráficos según los datos disponibles.