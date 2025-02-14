from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from dotenv import load_dotenv
import os

# Chargement des variables d'environnement
load_dotenv()

# Initialisation de l'application
app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'dev-key-à-changer-en-production')
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL', 'sqlite:///cinema.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialisation des extensions
db = SQLAlchemy(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'

# Import des routes après l'initialisation de l'application
from app import routes, models

# Création des tables de la base de données
with app.app_context():
    db.create_all()
