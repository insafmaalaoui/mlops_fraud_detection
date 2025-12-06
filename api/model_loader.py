import os
import pickle

def load_model():
    print("📌 Loading local pickle model...")

    # Chemin vers model.pkl
    model_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "models", "model.pkl")

    if not os.path.exists(model_path):
        raise FileNotFoundError(f"❌ model.pkl not found at: {model_path}")

    # Charger le modèle pickle
    with open(model_path, "rb") as f:
        model = pickle.load(f)

    print("✅ model.pkl loaded successfully!")
    return model
