# api/schemas.py
from pydantic import BaseModel
from typing import List, Optional, ClassVar


class Transaction(BaseModel):
    Time: float
    V1: float
    V2: float
    V3: float
    V4: float
    V5: float
    V6: float
    V7: float
    V8: float
    V9: float
    V10: float
    V11: float
    V12: float
    V13: float
    V14: float
    V15: float
    V16: float
    V17: float
    V18: float
    V19: float
    V20: float
    V21: float
    V22: float
    V23: float
    V24: float
    V25: float
    V26: float
    V27: float
    V28: float
    Amount: float

    # canonical feature order used in the dataset / training
    # Mark as ClassVar so Pydantic does not include it in the model schema/body
    FEATURE_ORDER: ClassVar[List[str]] = [
        "Time",
        "V1",
        "V2",
        "V3",
        "V4",
        "V5",
        "V6",
        "V7",
        "V8",
        "V9",
        "V10",
        "V11",
        "V12",
        "V13",
        "V14",
        "V15",
        "V16",
        "V17",
        "V18",
        "V19",
        "V20",
        "V21",
        "V22",
        "V23",
        "V24",
        "V25",
        "V26",
        "V27",
        "V28",
        "Amount",
    ]

    def to_dataframe(self):
        """Return a pandas DataFrame with original named columns (Time, V1.., Amount)."""
        try:
            import pandas as pd
        except Exception:
            raise
        return pd.DataFrame([self.dict()])

    def to_model_dataframe(self, model=None):
        """Return a DataFrame ready for the provided model.

        If `model` exposes `feature_names_in_` (sklearn), this will produce a
        DataFrame whose column names and ordering match the model's expectation.
        If `model` is None or has no `feature_names_in_`, returns the canonical
        named-columns DataFrame.
        """
        df = self.to_dataframe()
        if model is None:
            return df

        feat_in = getattr(model, "feature_names_in_", None)
        if feat_in is None:
            # some models store feature names as _feature_names_in
            feat_in = getattr(model, "_feature_names_in", None)

        if feat_in is None:
            return df

        # ensure strings
        feat_in = [str(f) for f in feat_in]

        # If model was trained on unnamed numeric columns (0,1,2,...), map
        # those positions to our canonical FEATURE_ORDER.
        try:
            # build values in the order of feat_in
            values = []
            for f in feat_in:
                # if feature name is numeric index like '0', '1', map by position
                if f.isdigit():
                    idx = int(f)
                    if idx < len(self.FEATURE_ORDER):
                        col_name = self.FEATURE_ORDER[idx]
                    else:
                        # fallback to using f as column name
                        col_name = f
                else:
                    col_name = f

                if col_name in df.columns:
                    values.append(df[col_name].iloc[0])
                else:
                    # missing feature: insert NaN
                    import numpy as _np

                    values.append(_np.nan)

            import pandas as pd

            return pd.DataFrame([values], columns=feat_in)
        except Exception:
            return df
