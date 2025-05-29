from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()  # Ensure the database instance is properly initialized

class AppConfig:
    def __init__(self):
        from flask import Flask
        from flask_restful import Api

        self.app = Flask(__name__)
        self.app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///../database/database.db"
        self.app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
        self.db = db
        self.api = Api(self.app)
