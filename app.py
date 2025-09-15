from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
from flask_sqlalchemy import SQLAlchemy
from models import db, Category, Service, Portfolio, SiteSettings, QuoteRequest, Contact
from admin import init_admin
import os
from dotenv import load_dotenv
import requests
from datetime import datetime

# Load environment variables
load_dotenv()

app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'dev-secret-key')
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL', 'sqlite:///araiza_inc.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize database
db.init_app(app)

# Initialize admin
init_admin(app)

def init_database_if_needed():
    """Initialize database with default data if needed"""
    try:
        # Create all tables
        db.create_all()
        
        # Check if categories already exist
        if Category.query.count() == 0:
            print("🔨 No data found, initializing database with default content...")
            
            # Create categories
            categories_data = [
                {"id": 1, "nombre": "Tecnología y Desarrollo", "descripcion": "Desarrollo de software, web y automatización"},
                {"id": 2, "nombre": "Telecomunicaciones y Telefonía", "descripcion": "Telefonía IP, VoIP, SMS y multicanal"},
                {"id": 3, "nombre": "Agencia de Viajes", "descripcion": "Boletos, tours, comisiones y seguros"},
                {"id": 4, "nombre": "Diseño Gráfico y Marketing", "descripcion": "Branding, publicidad digital y diseño"},
                {"id": 5, "nombre": "Electrónica y Proyectos DIY", "descripcion": "IoT, autos, CNC y hardware"},
                {"id": 6, "nombre": "Inteligencia Artificial y Data", "descripcion": "Modelos AI, chatbots, análisis de datos"}
            ]
            
            for cat_data in categories_data:
                category = Category(id=cat_data["id"], nombre=cat_data["nombre"], descripcion=cat_data["descripcion"])
                db.session.add(category)
            
            # Create services
            services_data = [
                {"id": 1, "id_categoria": 1, "nombre": "Desarrollo Web", "descripcion": "Sitios en WordPress, Divi, Flask, React, PHP"},
                {"id": 2, "id_categoria": 1, "nombre": "Aplicaciones AI", "descripcion": "Apps Flask con chatbots, WhatsApp, SMS, voz"},
                {"id": 3, "id_categoria": 1, "nombre": "Automatización n8n", "descripcion": "Flujos automáticos, integración con APIs"},
                {"id": 4, "id_categoria": 1, "nombre": "Bases de Datos", "descripcion": "MySQL, SQLite, FileMaker, reportes y APIs"},
                {"id": 5, "id_categoria": 1, "nombre": "DevOps & Hosting", "descripcion": "Proxmox, Vultr, Nginx, Docker, LXC, SSL"},
                {"id": 6, "id_categoria": 2, "nombre": "PBX y VoIP", "descripcion": "Asterisk, Issabel, LiveKit, Telnyx SIP Trunk"},
                {"id": 7, "id_categoria": 2, "nombre": "IVR y Call Routing", "descripcion": "Menús automáticos, grabaciones, AI en llamadas"},
                {"id": 8, "id_categoria": 2, "nombre": "SMS & WhatsApp", "descripcion": "Integración con Telnyx, WhatsApp Business API"},
                {"id": 9, "id_categoria": 3, "nombre": "Reservaciones y Boletos", "descripcion": "Amadeus, Sabre, consolidación de ventas"},
                {"id": 10, "id_categoria": 3, "nombre": "Tours y Paquetes", "descripcion": "Organización de viajes y experiencias"},
                {"id": 11, "id_categoria": 3, "nombre": "Seguros de Viaje", "descripcion": "Cotización automática y APIs de proveedores"},
                {"id": 12, "id_categoria": 3, "nombre": "Subagencias y Comisiones", "descripcion": "Reportes ARC, reglas de aerolíneas"},
                {"id": 13, "id_categoria": 4, "nombre": "Diseño Gráfico", "descripcion": "Logos, flyers, tarjetas, identidad visual"},
                {"id": 14, "id_categoria": 4, "nombre": "Marketing Digital", "descripcion": "SEO, redes sociales, MailerLite, campañas"},
                {"id": 15, "id_categoria": 5, "nombre": "Electrónica", "descripcion": "Microcontroladores, displays, sensores"},
                {"id": 16, "id_categoria": 5, "nombre": "IoT y DIY", "descripcion": "Arduino, ESP32, LoRa, sistemas HUD para autos"},
                {"id": 17, "id_categoria": 5, "nombre": "CNC y Mecatrónica", "descripcion": "CNC, IR touch frames, prototipos"},
                {"id": 18, "id_categoria": 6, "nombre": "Análisis de Datos", "descripcion": "Limpieza, clasificación, reportes inteligentes"},
                {"id": 19, "id_categoria": 6, "nombre": "Chatbots Multicanal", "descripcion": "Integración AI en WhatsApp, SMS, web"},
                {"id": 20, "id_categoria": 6, "nombre": "TinyML & ML", "descripcion": "Modelos ligeros para hardware embebido"}
            ]
            
            for serv_data in services_data:
                service = Service(id=serv_data["id"], id_categoria=serv_data["id_categoria"], 
                                nombre=serv_data["nombre"], descripcion=serv_data["descripcion"])
                db.session.add(service)
            
            # Create site settings
            site_settings_data = [
                {"key": "site_title", "value": "Araiza Inc", "description": "Título del sitio web"},
                {"key": "site_description", "value": "Soluciones tecnológicas integrales para tu empresa", "description": "Descripción del sitio"},
                {"key": "company_name", "value": "Araiza Inc", "description": "Nombre de la empresa"},
                {"key": "company_email", "value": "info@araizainc.com", "description": "Email de contacto"},
                {"key": "company_phone", "value": "+1 (555) 123-4567", "description": "Teléfono de contacto"},
                {"key": "company_address", "value": "123 Business Ave, Suite 100, City, State 12345", "description": "Dirección de la empresa"},
                {"key": "about_us", "value": "Araiza Inc es una empresa líder en soluciones tecnológicas...", "description": "Acerca de nosotros"},
                {"key": "facebook_url", "value": "https://facebook.com/araizainc", "description": "URL de Facebook"},
                {"key": "twitter_url", "value": "https://twitter.com/araizainc", "description": "URL de Twitter"},
                {"key": "linkedin_url", "value": "https://linkedin.com/company/araizainc", "description": "URL de LinkedIn"},
                {"key": "instagram_url", "value": "https://instagram.com/araizainc", "description": "URL de Instagram"},
                {"key": "logo_url", "value": "/static/images/logo.png", "description": "URL del logo"},
                {"key": "hero_title", "value": "Transformamos ideas en soluciones tecnológicas", "description": "Título principal del hero"},
                {"key": "hero_subtitle", "value": "Expertos en desarrollo, telecomunicaciones, IA y más", "description": "Subtítulo del hero"},
                {"key": "terms_conditions", "value": "Términos y condiciones de uso...", "description": "Términos y condiciones"},
                {"key": "privacy_policy", "value": "Política de privacidad...", "description": "Política de privacidad"},
                {"key": "accessibility", "value": "Declaración de accesibilidad...", "description": "Declaración de accesibilidad"}
            ]
            
            for setting_data in site_settings_data:
                setting = SiteSettings(key=setting_data["key"], value=setting_data["value"], description=setting_data["description"])
                db.session.add(setting)
            
            # Commit all changes
            db.session.commit()
            print("✅ Database initialized with default data successfully!")
        else:
            print("✅ Database already contains data")
            
    except Exception as e:
        print(f"❌ Error initializing database: {e}")
        db.session.rollback()
        raise

def get_site_setting(key, default=''):
    """Helper function to get site settings"""
    setting = SiteSettings.query.filter_by(key=key).first()
    return setting.value if setting else default

def get_categories_with_services():
    """Get categories with their services for navigation"""
    categories = Category.query.all()
    categories_with_services = []
    for category in categories:
        services = Service.query.filter_by(id_categoria=category.id, activo=True).all()
        categories_with_services.append({
            'category': category,
            'services': services
        })
    return categories_with_services

@app.context_processor
def inject_site_data():
    """Inject site data into all templates"""
    return {
        'site_title': get_site_setting('site_title', 'Araiza Inc'),
        'company_name': get_site_setting('company_name', 'Araiza Inc'),
        'company_email': get_site_setting('company_email'),
        'company_phone': get_site_setting('company_phone'),
        'company_address': get_site_setting('company_address'),
        'facebook_url': get_site_setting('facebook_url'),
        'twitter_url': get_site_setting('twitter_url'),
        'linkedin_url': get_site_setting('linkedin_url'),
        'instagram_url': get_site_setting('instagram_url'),
        'logo_url': get_site_setting('logo_url'),
        'categories_menu': get_categories_with_services()
    }

# Public Routes
@app.route('/')
def index():
    """Home page"""
    categories = Category.query.all()
    featured_services = Service.query.filter_by(activo=True).limit(6).all()
    featured_portfolio = Portfolio.query.filter_by(activo=True).limit(3).all()
    
    return render_template('index.html', 
                         categories=categories,
                         featured_services=featured_services,
                         featured_portfolio=featured_portfolio,
                         hero_title=get_site_setting('hero_title'),
                         hero_subtitle=get_site_setting('hero_subtitle'))

@app.route('/servicios')
def servicios():
    """Services page"""
    category_id = request.args.get('categoria')
    if category_id:
        services = Service.query.filter_by(id_categoria=category_id, activo=True).all()
        category = Category.query.get_or_404(category_id)
        selected_category = category
    else:
        services = Service.query.filter_by(activo=True).all()
        selected_category = None
    
    categories = Category.query.all()
    return render_template('servicios.html', 
                         services=services, 
                         categories=categories,
                         selected_category=selected_category)

@app.route('/servicio/<int:service_id>')
def servicio_detalle(service_id):
    """Service detail page"""
    service = Service.query.get_or_404(service_id)
    related_services = Service.query.filter(
        Service.id_categoria == service.id_categoria,
        Service.id != service.id,
        Service.activo == True
    ).limit(3).all()
    
    return render_template('servicio_detalle.html', 
                         service=service,
                         related_services=related_services)

@app.route('/portafolio')
def portafolio():
    """Portfolio page"""
    portfolio_items = Portfolio.query.filter_by(activo=True).all()
    return render_template('portafolio.html', portfolio_items=portfolio_items)

@app.route('/portafolio/<int:portfolio_id>')
def portafolio_detalle(portfolio_id):
    """Portfolio detail page"""
    portfolio_item = Portfolio.query.get_or_404(portfolio_id)
    return render_template('portafolio_detalle.html', portfolio_item=portfolio_item)

@app.route('/contacto')
def contacto():
    """Contact page"""
    return render_template('contacto.html')

@app.route('/contacto', methods=['POST'])
def contacto_post():
    """Handle contact form submission"""
    try:
        nombre = request.form.get('nombre')
        email = request.form.get('email')
        asunto = request.form.get('asunto')
        mensaje = request.form.get('mensaje')
        
        if not all([nombre, email, mensaje]):
            flash('Por favor complete todos los campos requeridos.', 'error')
            return redirect(url_for('contacto'))
        
        # Save to database
        contact = Contact(
            nombre=nombre,
            email=email,
            asunto=asunto,
            mensaje=mensaje
        )
        db.session.add(contact)
        db.session.commit()
        
        flash('¡Gracias por contactarnos! Te responderemos pronto.', 'success')
        return redirect(url_for('contacto'))
        
    except Exception as e:
        flash('Hubo un error al enviar tu mensaje. Por favor intenta de nuevo.', 'error')
        return redirect(url_for('contacto'))

@app.route('/cotizacion')
def cotizacion():
    """Quote request page"""
    categories = Category.query.all()
    return render_template('cotizacion.html', categories=categories)

@app.route('/cotizacion', methods=['POST'])
def cotizacion_post():
    """Handle quote request submission"""
    try:
        # Get form data
        nombre = request.form.get('nombre')
        email = request.form.get('email')
        telefono = request.form.get('telefono')
        empresa = request.form.get('empresa')
        categoria_id = request.form.get('categoria_id')
        servicio_id = request.form.get('servicio_id')
        mensaje = request.form.get('mensaje')
        presupuesto = request.form.get('presupuesto')
        fecha_limite = request.form.get('fecha_limite')
        
        if not all([nombre, email, mensaje]):
            flash('Por favor complete todos los campos requeridos.', 'error')
            return redirect(url_for('cotizacion'))
        
        # Convert date string to date object
        fecha_limite_obj = None
        if fecha_limite:
            try:
                fecha_limite_obj = datetime.strptime(fecha_limite, '%Y-%m-%d').date()
            except ValueError:
                pass
        
        # Save to database
        quote_request = QuoteRequest(
            nombre=nombre,
            email=email,
            telefono=telefono,
            empresa=empresa,
            categoria_id=categoria_id if categoria_id else None,
            servicio_id=servicio_id if servicio_id else None,
            mensaje=mensaje,
            presupuesto=presupuesto,
            fecha_limite=fecha_limite_obj
        )
        db.session.add(quote_request)
        db.session.commit()
        
        # Try to add to MailerLite (optional)
        try:
            add_to_mailerlite(email, nombre)
        except:
            pass  # Continue even if MailerLite fails
        
        flash('¡Solicitud de cotización enviada! Te contactaremos pronto.', 'success')
        return redirect(url_for('cotizacion'))
        
    except Exception as e:
        flash('Hubo un error al enviar tu solicitud. Por favor intenta de nuevo.', 'error')
        return redirect(url_for('cotizacion'))

@app.route('/api/servicios/<int:categoria_id>')
def api_servicios_categoria(categoria_id):
    """API endpoint to get services by category"""
    services = Service.query.filter_by(id_categoria=categoria_id, activo=True).all()
    return jsonify([{
        'id': service.id,
        'nombre': service.nombre,
        'descripcion': service.descripcion
    } for service in services])

def add_to_mailerlite(email, name):
    """Add subscriber to MailerLite"""
    api_key = os.getenv('MAILERLITE_API_KEY')
    group_id = os.getenv('MAILERLITE_GROUP_ID')
    
    if not api_key:
        return False
    
    url = "https://api.mailerlite.com/api/v2/subscribers"
    headers = {
        'X-MailerLite-ApiKey': api_key,
        'Content-Type': 'application/json'
    }
    
    data = {
        'email': email,
        'name': name,
        'groups': [group_id] if group_id else []
    }
    
    response = requests.post(url, json=data, headers=headers)
    return response.status_code == 200

# About, Terms, Privacy pages
@app.route('/acerca')
def acerca():
    """About page"""
    about_content = get_site_setting('about_us')
    return render_template('acerca.html', about_content=about_content)

@app.route('/terminos')
def terminos():
    """Terms and conditions page"""
    terms_content = get_site_setting('terms_conditions')
    return render_template('terminos.html', terms_content=terms_content)

@app.route('/privacidad')
def privacidad():
    """Privacy policy page"""
    privacy_content = get_site_setting('privacy_policy')
    return render_template('privacidad.html', privacy_content=privacy_content)

@app.route('/accesibilidad')
def accesibilidad():
    """Accessibility page"""
    accessibility_content = get_site_setting('accessibility')
    return render_template('accesibilidad.html', accessibility_content=accessibility_content)

if __name__ == '__main__':
    with app.app_context():
        try:
            print("📊 Araiza Inc Website")
            print("="*30)
            
            # Initialize database if needed
            init_database_if_needed()
            
            print("\n🚀 Starting Flask application...")
            print("📊 Website: http://localhost:5000")
            print("⚙️  Admin Panel: http://localhost:5000/admin")
            print("📝 Press Ctrl+C to stop\n")
            
            app.run(debug=True, host='0.0.0.0', port=5000)
            
        except Exception as e:
            print(f"❌ Error starting application: {e}")
            import traceback
            traceback.print_exc()