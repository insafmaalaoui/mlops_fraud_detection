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



2️⃣ Utilisation de Docker
Construire l’image Docker

Le Dockerfile.train permet de :

Installer Python et les dépendances.

Copier le code source.

Créer les dossiers nécessaires.

Définir le pipeline de training (pipeline_train.py) comme commande par défaut.

docker build -f Dockerfile.train -t fraud-train:latest .

Lancer le conteneur pour le training
# Mapper le dossier mlruns pour le suivi MLflow
docker run --rm -v ${PWD}/mlruns:/app/mlruns fraud-train:latest


⚠️ Note : pipeline_train.py est le fichier qui orchestre l’ensemble du pipeline (préprocessing, entraînement, sauvegarde du modèle et des métriques). Ne pas confondre avec train.py qui contient seulement la logique d’entraînement du modèle.

Lancer MLflow UI

Dans un terminal séparé, lancez MLflow pour visualiser les expérimentations :

mlflow ui


Puis ouvrez votre navigateur à http://127.0.0.1:5000
.

3️⃣ Tests unitaires

Des tests unitaires sont présents dans le dossier tests/ pour valider :

Le préprocessing des données (test_preprocessing.py).

L’entraînement du modèle (test_train.py).

Exécuter les tests
# Assurez-vous que PYTHONPATH inclut src
$env:PYTHONPATH="${PWD}\src"   # Windows PowerShell
# Linux / Mac: export PYTHONPATH="$(pwd)/src"

# Lancer les tests
python -m pytest -v tests/


Les tests permettent de vérifier que chaque composant ML fonctionne correctement indépendamment du pipeline complet.

# Ouvrir MLflow dans le navigateur
# http://127.0.0.1:5000

