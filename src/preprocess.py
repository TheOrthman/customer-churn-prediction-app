import pandas as pd

def prepare_data(df):
    df = df.copy()

    if "TotalCharges" in df.columns:
        df["TotalCharges"] = pd.to_numeric(df["TotalCharges"], errors="coerce")

    if "customerID" in df.columns:
        df = df.drop("customerID", axis=1)

    if "Churn" in df.columns:
        df = df.drop("Churn", axis=1)

    df = df.fillna(0)
    df = pd.get_dummies(df, drop_first=True)

    return df