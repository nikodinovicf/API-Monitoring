from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_restful import Api
from app.config import AppConfig, db  # Correctly imports SQLAlchemy instance


# Initialize Flask and configuration
app_config = AppConfig()
app = app_config.app
api = app_config.api

# Initialize SQLAlchemy
db.init_app(app)

# Import and register routes
from routes import routes_bp
app.register_blueprint(routes_bp)

# Initialize Flask-RESTful API
api.init_app(app)
