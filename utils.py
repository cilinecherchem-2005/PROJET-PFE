import pdfplumber
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# Chargement lazy de spacy
print("[INFO] Utilisation de spaCy pour analyse de texte")

def get_nlp():
    """Charger le modèle spaCy à la demande."""
    try:
        import spacy
        return spacy.load('fr_core_news_sm')
    except:
        print("[AVERTISSEMENT] Modèle spaCy non installé, analyse texte limitée")
        return None


# Fonctions utilitaires pour le backend

def extraire_texte_pdf(chemin_fichier):
    """Lire le texte d'un fichier PDF avec pdfplumber."""
    texte_total = ''
    with pdfplumber.open(chemin_fichier) as pdf:
        for page in pdf.pages:
            texte_total += page.extract_text() or ''
    return texte_total


def analyser_competences(texte):
    """Extraire les mots importants du texte pour l'analyse."""
    nlp = get_nlp()
    if nlp is None:
        # Si spacy n'est pas disponible, retourner le texte en minuscules
        return texte.lower()
    doc = nlp(texte)
    mots = []
    for token in doc:
        if not token.is_stop and token.is_alpha:
            mots.append(token.lemma_.lower())
    return ' '.join(mots)


def calculer_score(texte_cv, texte_offre):
    """Comparer le texte du CV et de l'offre pour obtenir un score."""
    vectorizer = TfidfVectorizer(stop_words='english')
    try:
        matrice = vectorizer.fit_transform([texte_cv, texte_offre])
        score = cosine_similarity(matrice[0:1], matrice[1:2])[0][0]
    except ValueError:
        score = 0

    # PostgreSQL/SQLAlchemy refuse parfois numpy.float64 : forcer un float Python natif
    return float(round(score * 100, 2))

