# Utiliser une image de base Python
FROM python:3.10-slim

# Définir le répertoire de travail
WORKDIR /tmp/fast_api

# Copier les fichiers de l'application dans le conteneur
COPY main.py .
COPY requirements.txt .
COPY utils ./utils

# Installer les dépendances
RUN apt-get update \
    && apt-get -y install libpq-dev gcc \
    && pip install --no-cache-dir -r requirements.txt \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Exposer le port utilisé par FastAPI
EXPOSE 8000

# Commande pour exécuter uvicorn
CMD ["uvicorn", "main:api", "--host", "0.0.0.0", "--port", "8000", "--reload"]