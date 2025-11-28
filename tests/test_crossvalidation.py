import os
import json
import pandas as pd
from src.crossvalidation import main

def test_crossvalidation_run(tmp_path, monkeypatch):
    """
    Teste l'exécution de crossvalidation.py dans un environnement isolé.
    """

    # --- 1. Création d'un dataset factice ---
    df = pd.DataFrame({
        "V1": [0.1, -0.2, 0.3, 0.4, -0.1],
        "V2": [1.1, 0.9, 1.0, 1.2, 1.3],
        "Amount": [10, 20, 30, 40, 50],
        "Class": [0, 1, 0, 0, 1]
    })

    # Répertoire temporaire pour éviter d’écrire dans ton vrai projet
    temp_data = tmp_path / "data" / "processed"
    temp_metrics = tmp_path / "metrics"
    temp_data.mkdir(parents=True)
    temp_metrics.mkdir(parents=True)

    # Sauvegarde du dataset factice
    fake_csv = temp_data / "cleaned.csv"
    df.to_csv(fake_csv, index=False)

    # --- 2. On redirige les chemins utilisés dans ton script ---
    monkeypatch.setenv("MLFLOW_TRACKING_URI", "file:" + str(tmp_path / "mlruns"))

    monkeypatch.chdir(tmp_path)
    os.makedirs("models", exist_ok=True)

    # --- 3. Exécution du main() ---
    main()

    # --- 4. Vérifications du fichier de métriques ---
    metrics_file = tmp_path / "metrics" / "cv_metrics.json"
    assert metrics_file.exists(), "Le fichier cv_metrics.json n'a pas été généré"

    with metrics_file.open() as f:
        metrics = json.load(f)

    assert "cv_f1" in metrics
    assert "f1_score" in metrics
    assert 0 <= metrics["cv_f1"] <= 1
    assert 0 <= metrics["f1_score"] <= 1
