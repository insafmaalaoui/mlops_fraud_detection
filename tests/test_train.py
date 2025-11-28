import os
import json
import shutil
import pandas as pd
from pathlib import Path

# On importe train.main() via src.train
from src.train import main as train_main

def make_cleaned_csv(tmp_path: Path):
    n = 200
    rng = None
    import numpy as np
    rng = np.random.RandomState(0)
    X = rng.randn(n, 5)
    df = pd.DataFrame(X, columns=[f"V{i}" for i in range(1, 6)])
    # ajouter Class équilibré
    df["Class"] = [0]*(n//2) + [1]*(n - n//2)
    # ensure directories
    processed_dir = tmp_path / "data" / "processed"
    processed_dir.mkdir(parents=True, exist_ok=True)
    out = processed_dir / "cleaned.csv"
    df.to_csv(out, index=False)
    return out

def test_train_creates_model_and_metrics(tmp_path):
    # Préparer un dossier data/processed/cleaned.csv dans tmp_path
    # On va exécuter train.main() dans la racine courante ; pour éviter collisions,
    # on change le cwd temporairement.
    project_root = Path.cwd()
    test_root = tmp_path / "project"
    shutil.copytree(project_root, test_root, dirs_exist_ok=True)

    # créer data/processed/cleaned.csv dans copy
    processed_dir = test_root / "data" / "processed"
    processed_dir.mkdir(parents=True, exist_ok=True)
    import numpy as np
    n = 200
    X = np.random.RandomState(1).randn(n, 5)
    df = pd.DataFrame(X, columns=[f"V{i}" for i in range(1, 6)])
    df["Class"] = [0]*(n//2) + [1]*(n - n//2)
    (processed_dir / "cleaned.csv").write_text(df.to_csv(index=False))

    # run train.main() inside test_root
    current_cwd = Path.cwd()
    try:
        os.chdir(test_root)
        # Remove potential previous outputs
        if (test_root / "models").exists():
            shutil.rmtree(test_root / "models")
        if (test_root / "metrics").exists():
            shutil.rmtree(test_root / "metrics")
        # Call training (this will write models/model.pkl and metrics/metrics.json)
        train_main()

        assert (test_root / "models" / "model.pkl").exists(), "Model file not created"
        assert (test_root / "metrics" / "metrics.json").exists(), "Metrics file not created"

        # Validate metrics file contains accuracy
        with open(test_root / "metrics" / "metrics.json", "r") as f:
            metrics = json.load(f)
        assert "accuracy" in metrics
    finally:
        os.chdir(current_cwd)
