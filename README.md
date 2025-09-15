# Araiza Inc Website

Una página web dinámica construida con Flask y SQLite para Araiza Inc, con panel de administración completo.

## Características

- **Página principal** con categorías de servicios
- **Servicios** organizados por categorías con páginas de detalle
- **Portafolio** de proyectos realizados
- **Formulario de cotización** integrado con MailerLite
- **Panel de administración** completo para gestionar contenido
- **Responsive design** compatible con móviles
- **Páginas legales** (términos, privacidad, accesibilidad)

## Instalación

### Requisitos Previos
- Python 3.8 o superior
- pip (gestor de paquetes de Python)

### Pasos de Instalación

1. **Instalar dependencias:**
```bash
pip install Flask==2.3.3 Flask-SQLAlchemy==3.0.5 python-dotenv==1.0.0 requests==2.31.0
```

2. **Configurar variables de entorno:**
Edita el archivo `.env` y actualiza las siguientes variables:
```
SECRET_KEY=tu-clave-secreta-aqui
MAILERLITE_API_KEY=tu-api-key-de-mailerlite
MAILERLITE_GROUP_ID=tu-group-id-de-mailerlite
```

3. **Ejecutar la aplicación:**
```bash
python app.py
```

4. **Acceder a la aplicación:**
- Sitio web: http://localhost:5000
- Panel de administración: http://localhost:5000/admin

## Estructura del Proyecto

```
├── app.py                 # Aplicación principal Flask
├── admin.py              # Panel de administración
├── models.py             # Modelos de base de datos
├── init_db.py            # Inicialización de la base de datos
├── requirements.txt      # Dependencias
├── .env                  # Variables de entorno
├── static/
│   ├── css/
│   │   └── style.css     # Estilos personalizados
│   ├── js/
│   │   └── main.js       # JavaScript personalizado
│   └── images/           # Imágenes del sitio
├── templates/
│   ├── base.html         # Plantilla base
│   ├── index.html        # Página principal
│   ├── servicios.html    # Página de servicios
│   ├── portafolio.html   # Página de portafolio
│   ├── contacto.html     # Página de contacto
│   ├── cotizacion.html   # Formulario de cotización
│   └── admin/            # Plantillas del panel de administración
└── araiza_inc.db         # Base de datos SQLite (se crea automáticamente)
```

## Configuración de MailerLite

1. Crea una cuenta en [MailerLite](https://www.mailerlite.com/)
2. Obtén tu API Key desde el panel de configuración
3. Crea un grupo para los suscriptores y obtén el Group ID
4. Actualiza las variables en el archivo `.env`

## Panel de Administración

El panel de administración te permite:

- **Gestionar Categorías:** Crear, editar y eliminar categorías de servicios
- **Gestionar Servicios:** Agregar servicios con imágenes, precios y descripciones
- **Gestionar Portafolio:** Subir proyectos con imágenes y detalles
- **Ver Cotizaciones:** Revisar y gestionar solicitudes de cotización
- **Ver Contactos:** Administrar mensajes de contacto
- **Configuración del Sitio:** Editar información de la empresa, redes sociales, etc.

## Funcionalidades Principales

### Para Visitantes:
- Navegación por categorías de servicios
- Visualización de portafolio de proyectos
- Solicitud de cotizaciones personalizadas
- Formulario de contacto
- Diseño responsivo para móviles

### Para Administradores:
- Dashboard con estadísticas
- Gestión completa de contenido
- Sistema de estados para cotizaciones y contactos
- Subida de imágenes para servicios y proyectos
- Configuración dinámica del sitio

## Personalización

### Modificar Categorías por Defecto
Edita el archivo `init_db.py` para cambiar las categorías y servicios que se crean automáticamente.

### Cambiar Estilos
Modifica el archivo `static/css/style.css` para personalizar la apariencia del sitio.

### Agregar Funcionalidades
Agrega nuevas rutas en `app.py` y crea las plantillas correspondientes en `templates/`.

## Soporte

Si necesitas ayuda con la configuración o personalización, contacta al equipo de desarrollo.

## Licencia

Este proyecto fue desarrollado específicamente para Araiza Inc.