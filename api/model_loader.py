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
            "151326182472059237",
            "models",
            "m-53db05ef3bfc4570ba3db7aaaef83d23",
            "artifacts",
        )
    )

    model = mlflow.sklearn.load_model(model_path)

    print("✅ Model loaded successfully!")
    return model