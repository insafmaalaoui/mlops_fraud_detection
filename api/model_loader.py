import mlflow
import os


def load_model():
    print("📌 Loading MLflow local model...")

    # Path pointing to the local mlruns model artifact directory
    model_path = os.path.abspath(
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

    model = mlflow.sklearn.load_model(model_path)

    print("✅ Model loaded successfully!")
    return model