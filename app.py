from backend import create_app

# Point d'entrée simple pour démarrer l'application
app = create_app()

if __name__ == '__main__':
    app.run(debug=True)
