# Utiliser une image de base Python
FROM python:3.10-slim

# Définir le répertoire de travail dans le conteneur
WORKDIR /tmp

# Copier les fichiers requis dans le conteneur
COPY query_form .
COPY requirements.txt . 
COPY activation.py .
RUN chmod +x /tmp/activation.py

# Installer les dépendances de votre application
RUN pip install --no-cache-dir -r requirements.txt

# Exposer le port utilisé par Streamlit
EXPOSE 8501

# Commande par défaut à exécuter lorsque le conteneur démarre
CMD ["streamlit", "run", "query_form.py", "--server.address", "0.0.0.0", "--server.port", "8501"]
