from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

class Category(db.Model):
    __tablename__ = 'categories'
    
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)
    descripcion = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationship with services
    services = db.relationship('Service', backref='category', lazy=True, cascade='all, delete-orphan')
    
    def __repr__(self):
        return f'<Category {self.nombre}>'

class Service(db.Model):
    __tablename__ = 'services'
    
    id = db.Column(db.Integer, primary_key=True)
    id_categoria = db.Column(db.Integer, db.ForeignKey('categories.id'), nullable=False)
    nombre = db.Column(db.String(100), nullable=False)
    descripcion = db.Column(db.Text)
    precio = db.Column(db.String(50))
    imagen = db.Column(db.String(200))
    activo = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def __repr__(self):
        return f'<Service {self.nombre}>'

class Portfolio(db.Model):
    __tablename__ = 'portfolio'
    
    id = db.Column(db.Integer, primary_key=True)
    titulo = db.Column(db.String(100), nullable=False)
    descripcion = db.Column(db.Text)
    imagen = db.Column(db.String(200))
    url = db.Column(db.String(200))
    cliente = db.Column(db.String(100))
    fecha_proyecto = db.Column(db.Date)
    tecnologias = db.Column(db.String(200))
    activo = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def __repr__(self):
        return f'<Portfolio {self.titulo}>'

class SiteSettings(db.Model):
    __tablename__ = 'site_settings'
    
    id = db.Column(db.Integer, primary_key=True)
    key = db.Column(db.String(50), unique=True, nullable=False)
    value = db.Column(db.Text)
    description = db.Column(db.String(200))
    
    def __repr__(self):
        return f'<SiteSettings {self.key}>'

class QuoteRequest(db.Model):
    __tablename__ = 'quote_requests'
    
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), nullable=False)
    telefono = db.Column(db.String(20))
    empresa = db.Column(db.String(100))
    categoria_id = db.Column(db.Integer, db.ForeignKey('categories.id'))
    servicio_id = db.Column(db.Integer, db.ForeignKey('services.id'))
    mensaje = db.Column(db.Text)
    presupuesto = db.Column(db.String(50))
    fecha_limite = db.Column(db.Date)
    estado = db.Column(db.String(20), default='pendiente')
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationships
    categoria = db.relationship('Category', backref='quote_requests')
    servicio = db.relationship('Service', backref='quote_requests')
    
    def __repr__(self):
        return f'<QuoteRequest {self.nombre} - {self.email}>'

class Contact(db.Model):
    __tablename__ = 'contacts'
    
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), nullable=False)
    asunto = db.Column(db.String(200))
    mensaje = db.Column(db.Text, nullable=False)
    estado = db.Column(db.String(20), default='nuevo')
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def __repr__(self):
        return f'<Contact {self.nombre} - {self.asunto}>'