from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify
from models import db, Category, Service, Portfolio, SiteSettings, QuoteRequest, Contact
from datetime import datetime
import os
from werkzeug.utils import secure_filename

admin_bp = Blueprint('admin', __name__, url_prefix='/admin')

# Helper function for file uploads
def allowed_file(filename):
    ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'webp'}
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def upload_file(file, folder='uploads'):
    """Upload file and return filename"""
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        # Add timestamp to avoid conflicts
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S_')
        filename = timestamp + filename
        
        upload_folder = os.path.join('static', 'images', folder)
        os.makedirs(upload_folder, exist_ok=True)
        
        file_path = os.path.join(upload_folder, filename)
        file.save(file_path)
        return f'/static/images/{folder}/{filename}'
    return None

# Admin Dashboard
@admin_bp.route('/')
def dashboard():
    """Admin dashboard"""
    stats = {
        'total_services': Service.query.count(),
        'active_services': Service.query.filter_by(activo=True).count(),
        'total_portfolio': Portfolio.query.count(),
        'active_portfolio': Portfolio.query.filter_by(activo=True).count(),
        'quote_requests': QuoteRequest.query.count(),
        'pending_quotes': QuoteRequest.query.filter_by(estado='pendiente').count(),
        'contacts': Contact.query.count(),
        'new_contacts': Contact.query.filter_by(estado='nuevo').count()
    }
    
    recent_quotes = QuoteRequest.query.order_by(QuoteRequest.created_at.desc()).limit(5).all()
    recent_contacts = Contact.query.order_by(Contact.created_at.desc()).limit(5).all()
    
    return render_template('admin/dashboard.html', 
                         stats=stats,
                         recent_quotes=recent_quotes,
                         recent_contacts=recent_contacts)

# Categories Management
@admin_bp.route('/categorias')
def categorias():
    """Manage categories"""
    categories = Category.query.all()
    return render_template('admin/categorias.html', categories=categories)

@admin_bp.route('/categorias/nueva', methods=['GET', 'POST'])
def nueva_categoria():
    """Create new category"""
    if request.method == 'POST':
        nombre = request.form.get('nombre')
        descripcion = request.form.get('descripcion')
        
        if not nombre:
            flash('El nombre es requerido.', 'error')
            return render_template('admin/categoria_form.html')
        
        categoria = Category(nombre=nombre, descripcion=descripcion)
        db.session.add(categoria)
        db.session.commit()
        
        flash('Categoría creada exitosamente.', 'success')
        return redirect(url_for('admin.categorias'))
    
    return render_template('admin/categoria_form.html')

@admin_bp.route('/categorias/<int:categoria_id>/editar', methods=['GET', 'POST'])
def editar_categoria(categoria_id):
    """Edit category"""
    categoria = Category.query.get_or_404(categoria_id)
    
    if request.method == 'POST':
        categoria.nombre = request.form.get('nombre')
        categoria.descripcion = request.form.get('descripcion')
        
        if not categoria.nombre:
            flash('El nombre es requerido.', 'error')
            return render_template('admin/categoria_form.html', categoria=categoria)
        
        db.session.commit()
        flash('Categoría actualizada exitosamente.', 'success')
        return redirect(url_for('admin.categorias'))
    
    return render_template('admin/categoria_form.html', categoria=categoria)

@admin_bp.route('/categorias/<int:categoria_id>/eliminar', methods=['POST'])
def eliminar_categoria(categoria_id):
    """Delete category"""
    categoria = Category.query.get_or_404(categoria_id)
    
    # Check if category has services
    if categoria.services:
        flash('No se puede eliminar una categoría que tiene servicios asociados.', 'error')
    else:
        db.session.delete(categoria)
        db.session.commit()
        flash('Categoría eliminada exitosamente.', 'success')
    
    return redirect(url_for('admin.categorias'))

# Services Management
@admin_bp.route('/servicios')
def servicios():
    """Manage services"""
    services = Service.query.all()
    return render_template('admin/servicios.html', services=services)

@admin_bp.route('/servicios/nuevo', methods=['GET', 'POST'])
def nuevo_servicio():
    """Create new service"""
    if request.method == 'POST':
        nombre = request.form.get('nombre')
        descripcion = request.form.get('descripcion')
        id_categoria = request.form.get('id_categoria')
        precio = request.form.get('precio')
        activo = 'activo' in request.form
        
        if not all([nombre, id_categoria]):
            flash('Nombre y categoría son requeridos.', 'error')
            categories = Category.query.all()
            return render_template('admin/servicio_form.html', categories=categories)
        
        # Handle image upload
        imagen_url = None
        if 'imagen' in request.files:
            file = request.files['imagen']
            if file.filename:
                imagen_url = upload_file(file, 'servicios')
        
        servicio = Service(
            nombre=nombre,
            descripcion=descripcion,
            id_categoria=id_categoria,
            precio=precio,
            imagen=imagen_url,
            activo=activo
        )
        db.session.add(servicio)
        db.session.commit()
        
        flash('Servicio creado exitosamente.', 'success')
        return redirect(url_for('admin.servicios'))
    
    categories = Category.query.all()
    return render_template('admin/servicio_form.html', categories=categories)

@admin_bp.route('/servicios/<int:servicio_id>/editar', methods=['GET', 'POST'])
def editar_servicio(servicio_id):
    """Edit service"""
    servicio = Service.query.get_or_404(servicio_id)
    
    if request.method == 'POST':
        servicio.nombre = request.form.get('nombre')
        servicio.descripcion = request.form.get('descripcion')
        servicio.id_categoria = request.form.get('id_categoria')
        servicio.precio = request.form.get('precio')
        servicio.activo = 'activo' in request.form
        
        if not all([servicio.nombre, servicio.id_categoria]):
            flash('Nombre y categoría son requeridos.', 'error')
            categories = Category.query.all()
            return render_template('admin/servicio_form.html', servicio=servicio, categories=categories)
        
        # Handle image upload
        if 'imagen' in request.files:
            file = request.files['imagen']
            if file.filename:
                imagen_url = upload_file(file, 'servicios')
                if imagen_url:
                    servicio.imagen = imagen_url
        
        db.session.commit()
        flash('Servicio actualizado exitosamente.', 'success')
        return redirect(url_for('admin.servicios'))
    
    categories = Category.query.all()
    return render_template('admin/servicio_form.html', servicio=servicio, categories=categories)

@admin_bp.route('/servicios/<int:servicio_id>/eliminar', methods=['POST'])
def eliminar_servicio(servicio_id):
    """Delete service"""
    servicio = Service.query.get_or_404(servicio_id)
    db.session.delete(servicio)
    db.session.commit()
    flash('Servicio eliminado exitosamente.', 'success')
    return redirect(url_for('admin.servicios'))

# Portfolio Management
@admin_bp.route('/portafolio')
def admin_portafolio():
    """Manage portfolio"""
    portfolio_items = Portfolio.query.all()
    return render_template('admin/portafolio.html', portfolio_items=portfolio_items)

@admin_bp.route('/portafolio/nuevo', methods=['GET', 'POST'])
def nuevo_portafolio():
    """Create new portfolio item"""
    if request.method == 'POST':
        titulo = request.form.get('titulo')
        descripcion = request.form.get('descripcion')
        url = request.form.get('url')
        cliente = request.form.get('cliente')
        fecha_proyecto = request.form.get('fecha_proyecto')
        tecnologias = request.form.get('tecnologias')
        activo = 'activo' in request.form
        
        if not titulo:
            flash('El título es requerido.', 'error')
            return render_template('admin/portafolio_form.html')
        
        # Convert date
        fecha_proyecto_obj = None
        if fecha_proyecto:
            try:
                fecha_proyecto_obj = datetime.strptime(fecha_proyecto, '%Y-%m-%d').date()
            except ValueError:
                pass
        
        # Handle image upload
        imagen_url = None
        if 'imagen' in request.files:
            file = request.files['imagen']
            if file.filename:
                imagen_url = upload_file(file, 'portfolio')
        
        portfolio_item = Portfolio(
            titulo=titulo,
            descripcion=descripcion,
            url=url,
            cliente=cliente,
            fecha_proyecto=fecha_proyecto_obj,
            tecnologias=tecnologias,
            imagen=imagen_url,
            activo=activo
        )
        db.session.add(portfolio_item)
        db.session.commit()
        
        flash('Proyecto agregado al portafolio exitosamente.', 'success')
        return redirect(url_for('admin.admin_portafolio'))
    
    return render_template('admin/portafolio_form.html')

@admin_bp.route('/portafolio/<int:portfolio_id>/editar', methods=['GET', 'POST'])
def editar_portafolio(portfolio_id):
    """Edit portfolio item"""
    portfolio_item = Portfolio.query.get_or_404(portfolio_id)
    
    if request.method == 'POST':
        portfolio_item.titulo = request.form.get('titulo')
        portfolio_item.descripcion = request.form.get('descripcion')
        portfolio_item.url = request.form.get('url')
        portfolio_item.cliente = request.form.get('cliente')
        portfolio_item.tecnologias = request.form.get('tecnologias')
        portfolio_item.activo = 'activo' in request.form
        
        # Convert date
        fecha_proyecto = request.form.get('fecha_proyecto')
        if fecha_proyecto:
            try:
                portfolio_item.fecha_proyecto = datetime.strptime(fecha_proyecto, '%Y-%m-%d').date()
            except ValueError:
                portfolio_item.fecha_proyecto = None
        
        if not portfolio_item.titulo:
            flash('El título es requerido.', 'error')
            return render_template('admin/portafolio_form.html', portfolio_item=portfolio_item)
        
        # Handle image upload
        if 'imagen' in request.files:
            file = request.files['imagen']
            if file.filename:
                imagen_url = upload_file(file, 'portfolio')
                if imagen_url:
                    portfolio_item.imagen = imagen_url
        
        db.session.commit()
        flash('Proyecto actualizado exitosamente.', 'success')
        return redirect(url_for('admin.admin_portafolio'))
    
    return render_template('admin/portafolio_form.html', portfolio_item=portfolio_item)

@admin_bp.route('/portafolio/<int:portfolio_id>/eliminar', methods=['POST'])
def eliminar_portafolio(portfolio_id):
    """Delete portfolio item"""
    portfolio_item = Portfolio.query.get_or_404(portfolio_id)
    db.session.delete(portfolio_item)
    db.session.commit()
    flash('Proyecto eliminado del portafolio exitosamente.', 'success')
    return redirect(url_for('admin.admin_portafolio'))

# Site Settings Management
@admin_bp.route('/configuracion')
def configuracion():
    """Site settings"""
    settings = SiteSettings.query.all()
    settings_dict = {setting.key: setting for setting in settings}
    return render_template('admin/configuracion.html', settings=settings_dict)

@admin_bp.route('/configuracion', methods=['POST'])
def actualizar_configuracion():
    """Update site settings"""
    for key, value in request.form.items():
        if key.startswith('setting_'):
            setting_key = key.replace('setting_', '')
            setting = SiteSettings.query.filter_by(key=setting_key).first()
            if setting:
                setting.value = value
            else:
                # Create new setting if it doesn't exist
                new_setting = SiteSettings(key=setting_key, value=value)
                db.session.add(new_setting)
    
    db.session.commit()
    flash('Configuración actualizada exitosamente.', 'success')
    return redirect(url_for('admin.configuracion'))

# Quote Requests Management
@admin_bp.route('/cotizaciones')
def cotizaciones():
    """Manage quote requests"""
    estado = request.args.get('estado', 'todas')
    page = request.args.get('page', 1, type=int)
    
    query = QuoteRequest.query
    if estado != 'todas':
        query = query.filter_by(estado=estado)
    
    quotes = query.order_by(QuoteRequest.created_at.desc()).paginate(
        page=page, per_page=20, error_out=False
    )
    
    return render_template('admin/cotizaciones.html', quotes=quotes, estado_filtro=estado)

@admin_bp.route('/cotizaciones/<int:quote_id>')
def ver_cotizacion(quote_id):
    """View quote request details"""
    quote = QuoteRequest.query.get_or_404(quote_id)
    return render_template('admin/cotizacion_detalle.html', quote=quote)

@admin_bp.route('/cotizaciones/<int:quote_id>/estado', methods=['POST'])
def actualizar_estado_cotizacion(quote_id):
    """Update quote request status"""
    quote = QuoteRequest.query.get_or_404(quote_id)
    nuevo_estado = request.form.get('estado')
    
    if nuevo_estado in ['pendiente', 'en_proceso', 'completada', 'cancelada']:
        quote.estado = nuevo_estado
        db.session.commit()
        flash('Estado actualizado exitosamente.', 'success')
    else:
        flash('Estado inválido.', 'error')
    
    return redirect(url_for('admin.ver_cotizacion', quote_id=quote_id))

# Contacts Management
@admin_bp.route('/contactos')
def contactos():
    """Manage contacts"""
    estado = request.args.get('estado', 'todos')
    page = request.args.get('page', 1, type=int)
    
    query = Contact.query
    if estado != 'todos':
        query = query.filter_by(estado=estado)
    
    contacts = query.order_by(Contact.created_at.desc()).paginate(
        page=page, per_page=20, error_out=False
    )
    
    return render_template('admin/contactos.html', contacts=contacts, estado_filtro=estado)

@admin_bp.route('/contactos/<int:contact_id>')
def ver_contacto(contact_id):
    """View contact details"""
    contact = Contact.query.get_or_404(contact_id)
    return render_template('admin/contacto_detalle.html', contact=contact)

@admin_bp.route('/contactos/<int:contact_id>/estado', methods=['POST'])
def actualizar_estado_contacto(contact_id):
    """Update contact status"""
    contact = Contact.query.get_or_404(contact_id)
    nuevo_estado = request.form.get('estado')
    
    if nuevo_estado in ['nuevo', 'leido', 'respondido', 'cerrado']:
        contact.estado = nuevo_estado
        db.session.commit()
        flash('Estado actualizado exitosamente.', 'success')
    else:
        flash('Estado inválido.', 'error')
    
    return redirect(url_for('admin.ver_contacto', contact_id=contact_id))

def init_admin(app):
    """Initialize admin blueprint"""
    app.register_blueprint(admin_bp)