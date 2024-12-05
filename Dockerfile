# Choisir une image de base officielle Python
FROM python:3.9

# Définir le répertoire de travail à l'intérieur du conteneur
WORKDIR /app

# Copier tous les fichiers locaux dans le répertoire de travail du conteneur
COPY . /app

# Installer les dépendances de l'application depuis requirements.txt
RUN pip install --upgrade pip && \
    pip install -r requirements.txt

# Exposer le port que Flask va utiliser
EXPOSE 80

# Commande pour démarrer l'application Flask
CMD ["gunicorn", "-b", "0.0.0.0:80", "app:app"]



