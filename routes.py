import os
from flask import render_template, request, redirect, url_for, flash, session
from backend import db
from models import Utilisateur, Offre, CV
from utils import extraire_texte_pdf, analyser_competences, calculer_score
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename

# Fonctions et routes principales de l'application

def est_connecte():
    """Vérifier si le recruteur est connecté."""
    return 'utilisateur_id' in session


def init_routes(app):
    @app.route('/')
    def index():
        if est_connecte():
            return redirect(url_for('dashboard'))
        return redirect(url_for('connexion'))

    @app.route('/connexion', methods=['GET', 'POST'])
    def connexion():
        if request.method == 'POST':
            email = request.form['email']
            mot_de_passe = request.form['mot_de_passe']
            utilisateur = Utilisateur.query.filter_by(email=email).first()
            if utilisateur and check_password_hash(utilisateur.mot_de_passe, mot_de_passe):
                session['utilisateur_id'] = utilisateur.id
                session['utilisateur_nom'] = utilisateur.nom
                flash('Connexion réussie', 'success')
                return redirect(url_for('dashboard'))
            flash('Email ou mot de passe incorrect', 'danger')
        return render_template('login.html')

    @app.route('/inscription', methods=['GET', 'POST'])
    def inscription():
        if request.method == 'POST':
            nom = request.form['nom']
            email = request.form['email']
            mot_de_passe = generate_password_hash(request.form['mot_de_passe'])
            existe = Utilisateur.query.filter_by(email=email).first()
            if existe:
                flash('Cet email existe déjà', 'warning')
            else:
                utilisateur = Utilisateur(nom=nom, email=email, mot_de_passe=mot_de_passe)
                db.session.add(utilisateur)
                db.session.commit()
                flash('Inscription réussie. Connectez-vous.', 'success')
                return redirect(url_for('connexion'))
        return render_template('register.html')

    @app.route('/deconnexion')
    def deconnexion():
        session.clear()
        flash('Déconnexion réussie', 'info')
        return redirect(url_for('connexion'))

    @app.route('/dashboard')
    def dashboard():
        if not est_connecte():
            return redirect(url_for('connexion'))

        offres = Offre.query.order_by(Offre.date.desc()).all()
        cvs = CV.query.order_by(CV.score.desc()).all()
        top_candidats = CV.query.order_by(CV.score.desc()).limit(5).all()
        total_offres = len(offres)
        total_cvs = CV.query.count()
        moyenne_score = round(sum([cv.score for cv in cvs]) / total_cvs, 2) if total_cvs else 0

        return render_template(
            'dashboard.html',
            offres=offres,
            cvs=cvs,
            top_candidats=top_candidats,
            total_offres=total_offres,
            total_cvs=total_cvs,
            moyenne_score=moyenne_score
        )

    @app.route('/offres', methods=['GET', 'POST'])
    def offres():
        if not est_connecte():
            return redirect(url_for('connexion'))

        if request.method == 'POST':
            titre = request.form['titre']
            description = request.form['description']
            competences = request.form['competences']
            nouvelle_offre = Offre(titre=titre, description=description, competences=competences)
            db.session.add(nouvelle_offre)
            db.session.commit()
            flash('Offre ajoutée avec succès', 'success')
            return redirect(url_for('offres'))

        offres = Offre.query.order_by(Offre.date.desc()).all()
        return render_template('offres.html', offres=offres)

    @app.route('/upload_cv', methods=['GET', 'POST'])
    def upload_cv():
        if not est_connecte():
            return redirect(url_for('connexion'))

        offres = Offre.query.all()
        if request.method == 'POST':
            offre_id = request.form.get('offre_id')
            fichiers = request.files.getlist('fichiers')
            if not fichiers:
                flash('Veuillez sélectionner au moins un fichier PDF', 'warning')
                return redirect(url_for('upload_cv'))

            for fichier in fichiers:
                if fichier.filename == '':
                    continue
                nom = secure_filename(fichier.filename)
                chemin = os.path.join(app.config['UPLOAD_FOLDER'], nom)
                os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
                fichier.save(chemin)

                texte = extraire_texte_pdf(chemin)
                texte_analyse = analyser_competences(texte)
                offre = Offre.query.get(int(offre_id)) if offre_id else None
                texte_offre = offre.description + ' ' + offre.competences if offre else ''
                score = calculer_score(texte_analyse, texte_offre) if offre else 0

                candidat = CV(nom_fichier=nom, texte=texte, score=score, offre_id=offre.id if offre else None)
                db.session.add(candidat)
                db.session.commit()

            flash('CV ajoutés et analysés', 'success')
            return redirect(url_for('upload_cv'))

        cvs = CV.query.order_by(CV.date.desc()).all()
        return render_template('upload_cv.html', offres=offres, cvs=cvs)

    @app.route('/candidats')
    def candidats():
        if not est_connecte():
            return redirect(url_for('connexion'))

        cvs = CV.query.order_by(CV.score.desc()).all()
        return render_template('candidats.html', cvs=cvs)
