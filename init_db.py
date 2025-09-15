#!/usr/bin/env python3
"""
Manual Database Initialization Script for Araiza Inc Website

This script is for manual database initialization only.
Normally, the database is automatically initialized when running app.py

Usage:
    python init_db.py
"""

from flask import Flask
from models import db
import os
from dotenv import load_dotenv

def manual_init():
    """Manual database initialization"""
    print("📊 Manual Database Initialization")
    print("Note: Database is normally auto-initialized by app.py")
    print("="*50)
    
    # Load environment variables
    load_dotenv()
    
    # Create Flask app
    app = Flask(__name__)
    app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'dev-secret-key')
    app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL', 'sqlite:///araiza_inc.db')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    
    # Initialize database
    db.init_app(app)
    
    with app.app_context():
        # Import the initialization function from app.py
        import sys
        sys.path.append('.')
        from app import init_database_if_needed
        
        init_database_if_needed()
        print("✅ Manual initialization completed!")
        print("🚀 You can now run: python app.py")

if __name__ == '__main__':
    manual_init()