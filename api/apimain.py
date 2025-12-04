# api/main.py
from fastapi import FastAPI
from api.schemas import Transaction
from api.model_loader import load_model
import pandas as pd
from api.logger import log_json

app = FastAPI(
    title="Fraud Detection API",
    description="API pour prédire les transactions frauduleuses",
    version="1.0.0"
)

# Load MLflow model once at start
model = load_model()

@app.get("/", tags=["Health Check"])
def home():
    return {"status": "API is running"}

@app.post("/predict", tags=["Prediction"])
def predict(data: Transaction):
    # Convertir JSON → DataFrame en respectant l'ordre des features attendu par le modèle
    try:
        df = data.to_model_dataframe(model)
    except Exception:
        # fallback to basic dict-based DataFrame
        df = pd.DataFrame([data.dict()])

    # Faire la prédiction
    prediction = model.predict(df)[0]
    #  AJOUTE LE LOG 
    log_json({
        "event": "prediction",
        "input": data.dict(),
        "prediction": int(prediction)
    })
    return {
        "fraud": int(prediction),
        "message": "Fraud detected" if prediction == 1 else "Transaction OK"
    }
