"""
Script de prédiction pour le modèle de détection de fraude
- Charge le modèle sauvegardé
- Prend en entrée un fichier CSV ou dictionnaire de features
- Retourne les prédictions
"""

import pickle
import pandas as pd
import os

MODEL_PATH = "models/model.pkl"  # Chemin vers le modèle entraîné

def load_model(model_path=MODEL_PATH):
    """Charger le modèle depuis le disque"""
    if not os.path.exists(model_path):
        raise FileNotFoundError(f"Modèle non trouvé à {model_path}")
    with open(model_path, "rb") as f:
        model = pickle.load(f)
    return model

def predict(model, X):
    """Faire des prédictions avec le modèle"""
    return model.predict(X)

def predict_from_csv(csv_path):
    """Prédire à partir d'un CSV"""
    df = pd.read_csv(csv_path)
    model = load_model()
    preds = predict(model, df)
    df['prediction'] = preds
    return df

if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Faire des prédictions avec le modèle de fraude")
    parser.add_argument("--input", type=str, required=True,
                        help="Chemin vers le CSV d'entrée pour la prédiction")
    parser.add_argument("--output", type=str, default="predictions.csv",
                        help="Chemin pour sauvegarder les prédictions")

    args = parser.parse_args()

    results = predict_from_csv(args.input)
    results.to_csv(args.output, index=False)
    print(f"✅ Prédictions sauvegardées dans {args.output}")
