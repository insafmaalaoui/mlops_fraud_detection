import os
import pickle

def load_model():
    print("📌 Loading local pickle model...")

<<<<<<< HEAD
    # Path pointing to the local mlruns model artifact directory
    model_path = os.path.abspath(
        os.path.join(
            os.path.dirname(__file__),
            "..",
            "mlruns",
            "151326182472059237",
            "models",
            "m-53db05ef3bfc4570ba3db7aaaef83d23",
            "artifacts",
        )
    )
=======
    # Chemin vers model.pkl
    model_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "models", "model.pkl")
>>>>>>> 39a6ef57106d28891aea6a8c442ec41559ec2bf1

    if not os.path.exists(model_path):
        raise FileNotFoundError(f"❌ model.pkl not found at: {model_path}")

    # Charger le modèle pickle
    with open(model_path, "rb") as f:
        model = pickle.load(f)

    print("✅ model.pkl loaded successfully!")
    return model
