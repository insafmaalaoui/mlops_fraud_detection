# api/main.py
from fastapi import FastAPI
from api.schemas import Transaction
from api.model_loader import load_model
import pandas as pd
from api.logger import log_json

# Evidently imports: make optional because different versions expose different
# symbols and the package may be absent in some environments. If unavailable
# we'll disable the drift endpoint gracefully.
try:
    from evidently.report import Report
    from evidently.metric_preset import DataDriftPreset
    _EVIDENTLY_AVAILABLE = True
except Exception:
    Report = None
    DataDriftPreset = None
    _EVIDENTLY_AVAILABLE = False




# ➕ Prometheus instrumentator (optional)
try:
    from prometheus_fastapi_instrumentator import Instrumentator
    _PROM_AVAILABLE = True
except Exception:
    Instrumentator = None
    _PROM_AVAILABLE = False


app = FastAPI(
    title="Fraud Detection API",
    description="API de détection de fraude avec monitoring",
    version="2.0.0"
)

# Charger modèle au démarrage
model = load_model()

# Buffer pour drift (on stocke les dernières prédictions)
prediction_history = []


# ----------------------------------------------------------------------
# 🌟 1. Endpoint Santé API
# ----------------------------------------------------------------------
@app.get("/", tags=["Health Check"])
@app.get("/monitoring/health", tags=["Monitoring"])
def health():
    return {"status": "API operational", "model_loaded": model is not None}


# ----------------------------------------------------------------------
# 🌟 2. Endpoint Prediction + LOGS + DRIFT BUFFER
# ----------------------------------------------------------------------
@app.post("/predict", tags=["Prediction"])
def predict(data: Transaction):

    # Convert JSON -> DataFrame
    try:
        df = data.to_model_dataframe(model)
    except Exception:
        df = pd.DataFrame([data.dict()])

    # If model is not loaded, return 503
    if model is None:
        return {"error": "Model not loaded"}, 503

    # Faire la prédiction
    prediction = model.predict(df)[0]

    # Sauvegarder pour Evidently Drift
    df_copy = df.copy()
    df_copy["prediction"] = int(prediction)
    prediction_history.append(df_copy)

    # Garder seulement les 200 dernières lignes
    if len(prediction_history) > 200:
        prediction_history.pop(0)

    # Logs JSON
    log_json({
        "event": "prediction",
        "input": data.dict(),
        "prediction": int(prediction)
    })

    return {
        "fraud": int(prediction),
        "message": "⚠️ Fraud détectée !" if prediction == 1 else "✔ Pas de fraude détectée."
    }


# ----------------------------------------------------------------------
# 🌟 3. Endpoint Evidently Drift Report
# ----------------------------------------------------------------------
@app.get("/monitoring/drift", tags=["Monitoring"])
def drift_report():

    if not _EVIDENTLY_AVAILABLE:
        return {
            "error": "Evidently is not available in this environment. Install 'evidently' to enable drift reports."
        }

    if len(prediction_history) < 30:
        return {"message": "Pas assez de données pour analyser le drift (minimum 30)."}

    df = pd.concat(prediction_history, ignore_index=True)

    # Build and run report (use small sample windows)
    try:
        report = Report(metrics=[DataDriftPreset()])
        report.run(reference_data=df.head(50), current_data=df.tail(50))
        return report.as_dict()
    except Exception as e:
        return {"error": "failed to build drift report", "detail": str(e)}


# ----------------------------------------------------------------------
# 🌟 4. Prometheus Metrics
# ----------------------------------------------------------------------
# Prometheus instrumentation must be added before the app starts serving.
# Do it at import time (module-level) so middleware is registered early.
if _PROM_AVAILABLE:
    try:
        Instrumentator().instrument(app).expose(app)
    except Exception:
        # If instrumentation fails for any reason, skip it to avoid breaking startup
        pass
