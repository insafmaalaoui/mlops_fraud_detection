"""
scripts/drift_detection.py

Usage example:
python scripts/drift_detection.py \
  --baseline data/processed/cleaned.csv \
  --current data/recent/recent_sample.csv \
  --output reports/drift_report \
  --mlflow-uri file:./mlruns
"""

import argparse
import os
import json
from pathlib import Path

import pandas as pd
import mlflow

# Evidently imports
from evidently.profile import Profile
from evidently.profile.sections import DataDriftProfileSection, TargetDriftProfileSection

def load_csv(path):
    return pd.read_csv(path)

def ensure_dir(path):
    Path(path).mkdir(parents=True, exist_ok=True)

def run_drift(baseline_path, current_path, output_dir, mlflow_uri=None, run_name="drift-check"):
    ensure_dir(output_dir)
    baseline = load_csv(baseline_path)
    current = load_csv(current_path)

    # Build profile with DataDrift and TargetDrift sections
    profile = Profile(sections=[DataDriftProfileSection(), TargetDriftProfileSection()])

    print("📌 Calculating drift profile (this may take a few seconds)...")
    profile.calculate(baseline_data=baseline, current_data=current)

    html_path = Path(output_dir) / "drift_report.html"
    json_path = Path(output_dir) / "drift_report.json"

    profile.save_html(str(html_path))
    profile.save_json(str(json_path))

    print(f"✅ Reports saved: {html_path}, {json_path}")

    # Optionally log the artifact to MLflow
    if mlflow_uri:
        mlflow.set_tracking_uri(mlflow_uri)
    try:
        with mlflow.start_run(run_name=run_name):
            mlflow.log_param("baseline", baseline_path)
            mlflow.log_param("current", current_path)
            mlflow.log_artifact(str(html_path), artifact_path="drift_reports")
            mlflow.log_artifact(str(json_path), artifact_path="drift_reports")
            print("📌 Drift reports logged to MLflow.")
    except Exception as e:
        print("⚠️ Warning: could not log to MLflow:", e)

    # Also return parsed JSON so caller/CI can inspect numbers
    with open(json_path, "r", encoding="utf-8") as f:
        report_json = json.load(f)

    return {"html": str(html_path), "json": str(json_path), "report": report_json}


def parse_args():
    p = argparse.ArgumentParser()
    p.add_argument("--baseline", required=True, help="Path to baseline CSV used for training.")
    p.add_argument("--current", required=True, help="Path to current/recent CSV to compare.")
    p.add_argument("--output", default="reports/drift_report", help="Output folder for reports.")
    p.add_argument("--mlflow-uri", default=None, help="MLflow tracking URI (e.g. file:./mlruns).")
    p.add_argument("--run-name", default="drift-check", help="MLflow run name.")
    return p.parse_args()

def main():
    args = parse_args()
    res = run_drift(
        baseline_path=args.baseline,
        current_path=args.current,
        output_dir=args.output,
        mlflow_uri=args.mlflow_uri,
        run_name=args.run_name
    )
    print("Finished. Outputs:", res["html"], res["json"])

if __name__ == "__main__":
    main()
