from models import db, Category, Service, SiteSettings
from datetime import datetime

def init_database(app):
    """Initialize database with sample data"""
    with app.app_context():
        # Create all tables
        db.create_all()
        
        # Check if categories already exist
        if Category.query.count() == 0:
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
                category = Category(
                    id=cat_data["id"],
                    nombre=cat_data["nombre"],
                    descripcion=cat_data["descripcion"]
                )
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
                service = Service(
                    id=serv_data["id"],
                    id_categoria=serv_data["id_categoria"],
                    nombre=serv_data["nombre"],
                    descripcion=serv_data["descripcion"]
                )
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
                setting = SiteSettings(
                    key=setting_data["key"],
                    value=setting_data["value"],
                    description=setting_data["description"]
                )
                db.session.add(setting)
            
            # Commit all changes
            db.session.commit()
            print("Database initialized with sample data!")