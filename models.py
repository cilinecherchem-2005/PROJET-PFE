from datetime import datetime
from backend import db

# Modèles de base de données simples

class Utilisateur(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nom = db.Column(db.String(120), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    mot_de_passe = db.Column(db.String(200), nullable=False)

class Offre(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    titre = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text, nullable=False)
    competences = db.Column(db.String(500), nullable=False)
    date = db.Column(db.DateTime, default=datetime.utcnow)

class CV(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nom_fichier = db.Column(db.String(200), nullable=False)
    texte = db.Column(db.Text, nullable=False)
    score = db.Column(db.Float, default=0)
    offre_id = db.Column(db.Integer, db.ForeignKey('offre.id'), nullable=True)
    date = db.Column(db.DateTime, default=datetime.utcnow)
