from fastapi import FastAPI
from api.schemas import Transaction
from api.model_loader import load_model
import pandas as pd
from api.logger import log_json

# NEW: monitoring
from prometheus_fastapi_instrumentator import Instrumentator

app = FastAPI(
    title="Fraud Detection API",
    description="API pour prédire les transactions frauduleuses",
    version="1.0.0"
)

# Monitoring Prometheus
Instrumentator().instrument(app).expose(app, endpoint="/metrics")

# Load model once
model = load_model()

@app.get("/", tags=["Health Check"])
def home():
    return {"status": "API is running"}

@app.post("/predict", tags=["Prediction"])
def predict(data: Transaction):

    try:
        df = data.to_model_dataframe(model)
    except Exception:
        df = pd.DataFrame([data.dict()])

    prediction = model.predict(df)[0]

    # Logging
    log_json({
        "event": "prediction",
        "input": data.dict(),
        "prediction": int(prediction)
    })

    return {
        "fraud": int(prediction),
        "message": "Fraud detected" if prediction == 1 else "Transaction OK"
    }
