#Commandes & installation du projet MLOps

## 1. Créer l’environnement virtuel
```bash
python -m venv .venv
.\.venv\Scripts\activate
pip install -r requirements.txt
pip install fastapi uvicorn # Installer FastAPI + Uvicor
pip install evidently #Installer Evidently (Monitoring Drift)
pip install prometheus-fastapi-instrumentator #Installer Prometheus Instrumentator
pip install streamlit requests #Installer Streamlit (interface UI)

uvicorn api.apimain:app --reload --port 8000  #Lancer FastAPI


#Tester l’endpoint /predict
curl -X POST "http://127.0.0.1:8000/predict" ^
-H "Content-Type: application/json" ^
-d "{\"amount\": 1200, \"oldbalanceOrg\": 5000, \"newbalanceOrig\": 3800}"
#Consulter le drift report
http://127.0.0.1:8000/monitoring/drift

#Lancer l’interface utilisateur (UI Streamlit)
streamlit run ui.py
