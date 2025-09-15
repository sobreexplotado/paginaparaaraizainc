from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
from flask_sqlalchemy import SQLAlchemy
from models import db, Category, Service, Portfolio, SiteSettings, QuoteRequest, Contact
from init_db import init_database
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
    try:
        # Initialize database on first run
        print("Initializing database...")
        init_database(app)
        print("Database initialized successfully!")
        
        print("Starting Flask application...")
        print("Website will be available at: http://localhost:5000")
        print("Admin panel will be available at: http://localhost:5000/admin")
        print("Press Ctrl+C to stop the server")
        
        app.run(debug=True, host='0.0.0.0', port=5000)
    except Exception as e:
        print(f"Error starting application: {e}")
        import traceback
        traceback.print_exc()