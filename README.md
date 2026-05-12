# Plateforme de recrutement intelligent

Application web professionnelle pour un projet de fin d'études, conçue pour un seul acteur : le recruteur.

## 📌 Description

Ce projet est une plateforme simple et moderne de gestion de recrutement. Le recruteur peut créer des offres, téléverser des CV PDF, analyser les compétences et générer un classement de candidats par compatibilité.

## ✨ Fonctionnalités principales

- Authentification recruteur (inscription / connexion)
- Tableau de bord avec statistiques et visualisation
- Création d'offres d'emploi
- Téléversement de plusieurs CV au format PDF
- Extraction automatique du texte des CV avec `pdfplumber`
- Analyse des compétences avec `spaCy`
- Calcul de score de compatibilité avec `scikit-learn`
- Classement des candidats par score
- Thème clair / sombre
- Sélection de langue : français, anglais, arabe
- Interface responsive avec Bootstrap 5

## 🛠️ Installation locale

1. Ouvrez PowerShell dans le dossier du projet.
2. Installez les dépendances :

```powershell
pip install -r requirements.txt
```

3. Installez le modèle spaCy :

```powershell
python -m spacy download en_core_web_sm
```

4. Créez la base de données MySQL :

```sql
CREATE DATABASE recrutement;
```

5. Configurez la variable d'environnement `DATABASE_URL` si nécessaire :

```powershell
setx DATABASE_URL "mysql+pymysql://user:password@localhost:3306/recrutement"
```

6. Configurez `SECRET_KEY` :

```powershell
setx SECRET_KEY "une_cle_secrete"
```

7. Lancez l'application :

```powershell
python app.py
```

8. Ouvrez le navigateur :

```text
http://127.0.0.1:5000
```

## ☁️ Déploiement Render

1. Poussez votre projet sur GitHub.
2. Créez un service Python sur Render.
3. Dans Render, définissez les commandes :
   - Build Command : `pip install -r requirements.txt`
   - Start Command : `gunicorn app:app`
4. Ajoutez ces variables d'environnement :
   - `DATABASE_URL`
   - `SECRET_KEY`
5. Déployez.

> Si Render fournit `mysql://...`, l'application convertit automatiquement en `mysql+pymysql://...`.

## 📁 Structure du projet

- `app.py` : point d'entrée de l'application
- `backend.py` : configuration de l'application Flask
- `models.py` : définition des tables
- `routes.py` : routes et logique principale
- `utils.py` : fonctions d'extraction et d'analyse
- `templates/` : pages HTML
- `static/css/style.css` : styles personnalisés
- `static/js/script.js` : script de thème et langue
- `requirements.txt` : dépendances Python
- `Procfile` : configuration de démarrage Render
- `schema.sql` : script de création de base de données

## 🚀 Utilisation

- Inscription du recruteur
- Création et gestion des offres d'emploi
- Téléversement de CV PDF
- Analyse automatique des CV
- Classement des candidats par compatibilité
- Changement de thème et de langue

## 📌 Conseils

- Vérifiez la configuration de votre base MySQL avant de lancer l'application.
- Pour un déploiement réel, utilisez une base de données distante et définissez bien `DATABASE_URL`.
- N'oubliez pas de garder `SECRET_KEY` privé.
