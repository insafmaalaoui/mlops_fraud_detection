import os
import pandas as pd
import numpy as np
from src.preprocessing import preprocess_data

def make_dummy_df(n=100):
    # Générer un petit dataset équilibré avec 5 features + Class
    rng = np.random.RandomState(42)
    X = rng.randn(n, 5)
    df = pd.DataFrame(X, columns=[f"V{i}" for i in range(1, 6)])
    # équilibrer les classes (50/50)
    df["Class"] = [0]*(n//2) + [1]*(n - n//2)
    return df

def test_preprocess_returns_cleaned_with_class():
    df = make_dummy_df(100)
    df_clean = preprocess_data(df)
    # Doit contenir la colonne Class
    assert "Class" in df_clean.columns
    # Doit avoir au moins 1 ligne
    assert df_clean.shape[0] > 0
    # Cols should be features + Class
    assert df_clean.shape[1] >= 2
