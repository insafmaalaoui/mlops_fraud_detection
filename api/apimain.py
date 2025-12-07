from fastapi import FastAPI
from api.schemas import Transaction
from api.model_loader import load_model
import pandas as pd
from api.logger import log_json


# ------------------------------------------------------------------------------
# 🔹 Evidently (optionnel)
# ------------------------------------------------------------------------------
try:
    from evidently.report import Report
    from evidently.metric_preset import DataDriftPreset
    _EVIDENTLY_AVAILABLE = True
except Exception:
    Report = None
    DataDriftPreset = None
    _EVIDENTLY_AVAILABLE = False


# ------------------------------------------------------------------------------
# 🔹 Prometheus (optionnel)
# ------------------------------------------------------------------------------
try:
    from prometheus_fastapi_instrumentator import Instrumentator
    _PROM_AVAILABLE = True
except Exception:
    Instrumentator = None
    _PROM_AVAILABLE = False


# ------------------------------------------------------------------------------
# 🌟 Init FastAPI
# ------------------------------------------------------------------------------
app = FastAPI(
    title="Fraud Detection API",
    description="API de détection de fraude avec monitoring",
    version="2.0.0"
)


# ------------------------------------------------------------------------------
# 🌟 Load modèle une seule fois
# ------------------------------------------------------------------------------
model = load_model()

# Buffer pour stocker les prédictions (pour Evidently)
prediction_history = []


# ------------------------------------------------------------------------------
# 🌟 1. Health Check
# ------------------------------------------------------------------------------
@app.get("/", tags=["Health Check"])
@app.get("/monitoring/health", tags=["Monitoring"])
def health():
    return {"status": "API operational", "model_loaded": model is not None}


# ------------------------------------------------------------------------------
# 🌟 2. Prediction + Logs + Drift Buffer
# ------------------------------------------------------------------------------
@app.post("/predict", tags=["Prediction"])
def predict(data: Transaction):

    try:
        df = data.to_model_dataframe(model)
    except Exception:
        df = pd.DataFrame([data.dict()])

    if model is None:
        return {"error": "Model not loaded"}, 503

    prediction = model.predict(df)[0]

    # Sauvegarde dans le buffer drift
    df_copy = df.copy()
    df_copy["prediction"] = int(prediction)
    prediction_history.append(df_copy)

    # Buffer max = 200 lignes
    if len(prediction_history) > 200:
        prediction_history.pop(0)

    # Log JSON
    log_json({
        "event": "prediction",
        "input": data.dict(),
        "prediction": int(prediction)
    })

    return {
        "fraud": int(prediction),
        "message": "⚠️ Fraud détectée !" if prediction == 1 else "✔ Pas de fraude détectée."
    }


# ------------------------------------------------------------------------------
# 🌟 3. Evidently Drift Report
# ------------------------------------------------------------------------------
@app.get("/monitoring/drift", tags=["Monitoring"])
def drift_report():

    if not _EVIDENTLY_AVAILABLE:
        return {
            "error": "Evidently is not available. Install 'evidently' to enable drift reports."
        }

    if len(prediction_history) < 30:
        return {"message": "Pas assez de données pour analyser le drift (minimum 30)."}

    df = pd.concat(prediction_history, ignore_index=True)

    try:
        report = Report(metrics=[DataDriftPreset()])
        report.run(reference_data=df.head(50), current_data=df.tail(50))
        return report.as_dict()
    except Exception as e:
        return {"error": "failed to build drift report", "detail": str(e)}


# ------------------------------------------------------------------------------
# 🌟 4. Prometheus Metrics
# ------------------------------------------------------------------------------
if _PROM_AVAILABLE:
    try:
        Instrumentator().instrument(app).expose(app)
    except Exception:
        pass
