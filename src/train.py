import pandas as pd
import pickle
import json
import mlflow
import mlflow.sklearn
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
from sklearn.ensemble import RandomForestClassifier
from mlflow.models import infer_signature
import os

def main():
    mlflow.set_tracking_uri("file:./mlruns")

    os.makedirs("mlruns/.trash", exist_ok=True)

    mlflow.set_experiment("fraud_detection")

    print("📌 Loading processed dataset...")
    df = pd.read_csv("data/processed/cleaned.csv")

    X = df.drop("Class", axis=1)
    y = df["Class"]

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42
    )

    print("📌 Training Random Forest...")

    with mlflow.start_run():
        model = RandomForestClassifier(
            n_estimators=150,
            max_depth=10,
            random_state=42
        )

        model.fit(X_train, y_train)
        y_pred = model.predict(X_test)

        acc = accuracy_score(y_test, y_pred)
        print(f"✅ Accuracy: {acc}")

        mlflow.log_param("n_estimators", 150)
        mlflow.log_param("max_depth", 10)
        mlflow.log_metric("accuracy", acc)

        signature = infer_signature(X_train, y_pred)

        mlflow.sklearn.log_model(
            sk_model=model,
            artifact_path="rf_model",
            signature=signature,
            input_example=X_train.iloc[:5]
        )

        print("📌 MLflow: Model logged!")

        os.makedirs("models", exist_ok=True)
        os.makedirs("metrics", exist_ok=True)

        with open("models/model.pkl", "wb") as f:
            pickle.dump(model, f)

        with open("metrics/metrics.json", "w") as f:
            json.dump({"accuracy": acc}, f)

if __name__ == "__main__":
    main()
