import json
import pandas as pd
import mlflow
import mlflow.sklearn
from sklearn.model_selection import GridSearchCV, StratifiedKFold
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, f1_score
from mlflow.models import infer_signature

def main():
    print("📌 Loading processed dataset for cross-validation...")
    df = pd.read_csv("data/processed/cleaned.csv")

    X = df.drop("Class", axis=1)
    y = df["Class"]

    # -------------------------
    # 🔥 Param grid (rapide)
    # -------------------------
    param_grid = {
        "n_estimators": [80, 120],
        "max_depth": [6, 8],
    }

    cv = StratifiedKFold(n_splits=3, shuffle=True, random_state=42)

    model = RandomForestClassifier(random_state=42, n_jobs=-1)

    grid = GridSearchCV(
        estimator=model,
        param_grid=param_grid,
        cv=cv,
        scoring="f1",
        n_jobs=-1,
        verbose=0
    )

    # -------------------------
    # 🔥 MLflow
    # -------------------------
    mlflow.set_tracking_uri("file:./mlruns")
    mlflow.set_experiment("fraud_detection_cv")

    with mlflow.start_run():

        print("📌 Running GridSearchCV (FAST MODE)...")
        grid.fit(X, y)

        best_model = grid.best_estimator_
        best_params = grid.best_params_
        best_score = grid.best_score_

        print("🎯 Best F1:", best_score)
        print("🏆 Best Params:", best_params)

        # Prediction
        y_pred = best_model.predict(X)
        f1 = f1_score(y, y_pred)

        # -------------------------
        # 🔥 MLflow logging
        # -------------------------
        mlflow.log_params(best_params)
        mlflow.log_metric("cv_f1", best_score)
        mlflow.log_metric("f1_score", f1)

        signature = infer_signature(X, y_pred)

        mlflow.sklearn.log_model(
            sk_model=best_model,
            artifact_path="rf_cv_model",
            signature=signature,
            input_example=X.iloc[:3],
        )

        print("📌 MLflow: CV model logged!")

        # -------------------------
        # 🔥 Save metrics for DVC
        # -------------------------
        metrics = {
            "cv_f1": float(best_score),
            "f1_score": float(f1)
        }

        with open("metrics/cv_metrics.json", "w") as f:
            json.dump(metrics, f, indent=4)

        print("📌 metrics/cv_metrics.json saved!")

if __name__ == "__main__":
    main()
