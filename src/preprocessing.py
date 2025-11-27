import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
import os

RAW_DATA_PATH = "data/raw/creditcard.csv"
PROCESSED_DATA_PATH = "data/processed"

def load_data():
    """Load dataset"""
    return pd.read_csv(RAW_DATA_PATH)

def preprocess_data(df):
    """Clean + Scale dataset"""
    # Remove missing values
    df = df.dropna()

    # Separate features and target
    X = df.drop("Class", axis=1)
    y = df["Class"]

    # Normalize numerical columns
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)

    # Split Train/Test for later evaluation
    X_train, X_test, y_train, y_test = train_test_split(
        X_scaled, y, test_size=0.2, random_state=42, stratify=y
    )

    # Create a clean dataset format
    df_clean = pd.DataFrame(X_train)
    df_clean["Class"] = y_train.values

    return df_clean


def save_processed_data(df_clean):
    """Save preprocessed dataset"""
    os.makedirs(PROCESSED_DATA_PATH, exist_ok=True)
    output_path = os.path.join(PROCESSED_DATA_PATH, "cleaned.csv")
    df_clean.to_csv(output_path, index=False)
    print(f"Data saved successfully → {output_path}")


if __name__ == "__main__":
    print("📌 Starting preprocessing...")

    df = load_data()
    df_clean = preprocess_data(df)
    save_processed_data(df_clean)

    print("✨ Preprocessing complete!")
