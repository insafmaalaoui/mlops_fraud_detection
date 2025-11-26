import pandas as pd
from sklearn.preprocessing import StandardScaler
import os

def main():
    raw_path = "data/raw/creditcard.csv"
    processed_path = "data/processed"
    output_file = f"{processed_path}/cleaned.csv"

    # Create folders if not exist
    os.makedirs(processed_path, exist_ok=True)

    print("📌 Loading raw dataset...")
    df = pd.read_csv(raw_path)

    # Standardize Amount column
    scaler = StandardScaler()
    df["Amount"] = scaler.fit_transform(df["Amount"].values.reshape(-1, 1))

    print("📌 Saving cleaned dataset...")
    df.to_csv(output_file, index=False)
    print(f"✅ Done: {output_file}")

if __name__ == "__main__":
    main()
