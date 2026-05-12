import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import spacy

# Création de l'objet de base de données
# Ce fichier contient la configuration Flask et SQLAlchemy

db = SQLAlchemy()

# Chargement du modèle spaCy pour l'analyse de texte
# Ce modèle sera chargé seulement quand nécessaire
if __name__ != '__main__':
    try:
        import spacy
        nlp = spacy.load('en_core_web_sm')
    except:
        nlp = None


def create_app():
    """Créer et configurer l'application Flask."""
    app = Flask(__name__, template_folder='templates', static_folder='static')
    app.secret_key = os.environ.get('SECRET_KEY', 'cle_secrete_pour_session')
    db_url = os.environ.get('DATABASE_URL', 'mysql+pymysql://recruteur:motdepasse@localhost/recrutement')
    if db_url.startswith('mysql://'):
        db_url = db_url.replace('mysql://', 'mysql+pymysql://', 1)
    app.config['SQLALCHEMY_DATABASE_URI'] = db_url
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['UPLOAD_FOLDER'] = os.path.join(os.path.dirname(__file__), 'static', 'uploads')
    app.config['MAX_CONTENT_LENGTH'] = 20 * 1024 * 1024  # 20MB

    db.init_app(app)

    # Importer les modules de modèle et routes après la création de l'application
    with app.app_context():
        import models
        from routes import init_routes
        init_routes(app)
        db.create_all()

    return app
