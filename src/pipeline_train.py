#!/usr/bin/env python3
"""
Pipeline d'entraînement reproductible :
- Charge les données brutes
- Prétraite et sauvegarde data/processed/cleaned.csv
- Lance train.main() pour entraîner, logger MLflow et sauvegarder le modèle/metrics
Usage:
    python src/pipeline_train.py
"""
import os
import sys
from pathlib import Path

# Garantir que src/ est dans le path pour importer preprocessing & train
this_dir = Path(__file__).resolve().parent
sys.path.insert(0, str(this_dir))

from preprocessing import load_data, preprocess_data, save_processed_data
from train import main as train_main

def run_pipeline():
    print("🚀 Démarrage pipeline d'entraînement reproductible")

    # 1) Charger les données raw
    print("📌 Chargement des données brutes...")
    df_raw = load_data()
    print(f"✅ Raw data shape: {df_raw.shape}")

    # 2) Preprocessing
    print("📌 Exécution du preprocessing...")
    df_clean = preprocess_data(df_raw)
    print(f"✅ Preprocessing terminé - cleaned shape: {df_clean.shape}")

    # 3) Sauvegarder les données prétraitées (pour train.py)
    save_processed_data(df_clean)
    print("✅ Données prétraitées sauvegardées dans data/processed/cleaned.csv")

    # 4) Lancer l'entraînement (train.py)
    print("📌 Lancement du training (train.py)...")
    train_main()
    print("✅ Training terminé")

    print("🎉 Pipeline terminé avec succès!")

if __name__ == "__main__":
    run_pipeline()
