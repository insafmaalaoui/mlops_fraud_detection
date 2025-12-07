import os
import pickle


def load_model():
<<<<<<< HEAD
    """Attempt to load the ML model.

    Priority:
    1. Load with mlflow if available and a tracked model exists
    2. Fallback to loading a pickle at `models/model.pkl`
    Returns the model object or None if not found.
    """
    print("📌 Loading model (mlflow if available, else pickle)...")

    # try mlflow first (lazy import to avoid ImportError at module import time)
    try:
        import mlflow

        # Path pointing to the local mlruns model artifact directory (if present)
        mlflow_model_path = os.path.abspath(
            os.path.join(
                os.path.dirname(__file__),
                "..",
                "mlruns",
                "443060123017548317",
                "models",
                "m-4ae4f1e1d8314af2b603a426d684ea9e",
                "artifacts",
            )
        )

        if os.path.exists(mlflow_model_path):
            model = mlflow.sklearn.load_model(mlflow_model_path)
            print("✅ Model loaded successfully via MLflow!")
            return model
    except Exception:
        # mlflow not available or failed to load — we'll fallback below
        pass

    # Fallback: try loading a pickle model saved by training script
    pickle_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "models", "model.pkl"))
    if os.path.exists(pickle_path):
        try:
            with open(pickle_path, "rb") as f:
                model = pickle.load(f)
            print(f"✅ Model loaded from pickle: {pickle_path}")
            return model
        except Exception:
            print(f"⚠️ Failed to load pickle model from {pickle_path}")

    print("⚠️ No model found (mlflow missing or model artifact absent). Continuing without model.")
    return None
=======
>>>>>>> 01845279f501c3673a6eadf46a80d18b306d4e1c
    print("📌 Loading local pickle model...")

    # Chemin vers model.pkl dans dossier /models
    model_path = os.path.join(
        os.path.dirname(os.path.dirname(__file__)),
        "models",
        "model.pkl"
    )

    if not os.path.exists(model_path):
        raise FileNotFoundError(f"❌ model.pkl not found at: {model_path}")

    # Charger le modèle pickle
    with open(model_path, "rb") as f:
        model = pickle.load(f)

    print("✅ model.pkl loaded successfully!")
<<<<<<< HEAD
    return model
=======
    return model
>>>>>>> 01845279f501c3673a6eadf46a80d18b306d4e1c
