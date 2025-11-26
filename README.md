# MLOps Fraud Detection

## Description
Ce projet implémente un système de détection de fraudes sur les transactions financières.  
Il utilise les bonnes pratiques MLOps avec **DVC** pour le versioning des données et modèles, et **MLflow** pour le tracking des expériences.  

---



## Installation et configuration

Toutes les commandes pour installer et configurer le projet :

```bash
# Cloner le dépôt Git
git clone https://github.com/insafmaalaoui/mlops_fraud_detection.git

# Se déplacer dans le dossier du projet
cd mlops_fraud_detection

# Activer l'environnement virtuel (Windows)
.\venv\Scripts\activate

# Installer les dépendances
pip install -r requirements.txt

# Récupérer les datasets et modèles versionnés via DVC
dvc pull

# Lancer un script Python (exemple : entraînement)
python src/train.py

# Lancer MLflow UI dans un autre terminal
mlflow ui

# Ouvrir MLflow dans le navigateur
# http://127.0.0.1:5000
