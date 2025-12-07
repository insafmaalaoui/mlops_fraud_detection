Déploiement & Monitoring du Modèle de Détection de Fraude :

Ce document décrit le travail qu'on a réalisé dans la partie Déploiement, CI/CD, Monitoring et Maintenance du modèle du projet de détection de fraude.
Il se concentre uniquement sur la partie MLOps (pas l’entraînement ML).

1. Mise en place de l’API d’inférence :

Création d’une API FastAPI :

On a développé une API dédiée à l’inférence du modèle :

* FastAPI pour l'exposition de l’endpoint /predict
* Chargement du modèle
* Prétraitement automatique des données reçues
* Retour d'une prédiction
* Ajout du logging JSON

Fichier principal : api/apimain.py

Exemple d’inférence :

POST http://localhost:8000/predict

{
  "Time": 100,
  "V1": -1.1,
  "V2": 0.5,
  "V3": -2.4,
  "V4": 0.7,
  "V5": -1.1,
  "V6": 0.2,
  "V7": -0.9,
  "V8": 0.1,
  "V9": 0.2,
  "V10": -0.4,
  "V11": 0.5,
  "V12": -1.5,
  "V13": 0.9,
  "V14": -0.3,
  "V15": 0.2,
  "V16": -0.4,
  "V17": 0.1,
  "V18": -0.7,
  "V19": 0.3,
  "V20": -0.4,
  "V21": 0.6,
  "V22": -0.2,
  "V23": 0.3,
  "V24": 0.2,
  "V25": -0.9,
  "V26": 0.5,
  "V27": 0.1,
  "V28": -0.1,
  "Amount": 45
}

2. Conteneurisation avec Docker :

On a créé une image dédiée à l’inférence du modèle :

* Dockerfile propre (Dockerfile.inference)
* Installation des dépendances
* Copie de l’API et du modèle
* Exposition du port 8000

docker compose up --build -d

Conteneur obtenu : fraud_api_container → API d’inférence

3. Création des pipelines CI/CD :

On a configuré un pipeline pour :

✔ Lancer automatiquement des tests

✔ Valider et reconstruire l’image Docker

✔ Déployer la nouvelle version de l’API

Technologies :

* GitHub Actions
* Build → Test → Docker Build & Push → Déploiement

Fichier : .github/workflows/api_inference.yml

4. Mise en place du Monitoring : Prometheus & Grafana :

On a ajouté un monitoring complet basé sur :

✔ Prometheus

* Scraping automatique des métriques de l’API
* Endpoint /metrics ajouté via : prometheus_fastapi_instrumentator
* Export des métriques :
  * http_request_duration_seconds_
  * http_requests_total
  * Latence
  * Codes HTTP
  * Temps d'exécution des prédictions

✔ Grafana

* Ajout de Prometheus comme data source
* Création d’un dashboard personnalisé :

  * taux d’erreur
  * latence moyenne API
  * nombre de requêtes par endpoint
  * statut du service en temps réel

5. Tests de fonctionnement réalisés :

Test API : http://localhost:8000/docs

Test Docker : docker ps

Test Prometheus : http://localhost:9090/targets → Statut : UP

Test Grafana : http://localhost:3000 → Dashboard opérationnel

→ Résultat final :

On a réussi à mettre en place entièrement :

✔ Un service d’inférence stable
✔ Une image Docker professionnelle
✔ Un pipeline CI/CD automatisé
✔ Un monitoring complet (Prometheus + Grafana)
✔ Un dashboard temps réel pour surveiller l’API