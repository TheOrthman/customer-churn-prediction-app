import streamlit as st
import pandas as pd
import joblib
from src.preprocess import prepare_data

st.set_page_config(page_title="Customer Churn Prediction", layout="wide")

st.title("📉 Customer Churn Prediction App")

st.markdown("""
This app predicts which customers are likely to churn based on customer account, service, and billing information.

### How it works
- Upload a customer CSV file with the same structure as the Telco Customer Churn dataset
- The model predicts churn probability for each customer
- Adjust the threshold to control how sensitive the model is

**Tip:** Lower threshold = catches more possible churners, but may increase false alarms.
""")

st.subheader("📌 Expected CSV Columns")

expected_columns = [
    "customerID", "gender", "SeniorCitizen", "Partner", "Dependents",
    "tenure", "PhoneService", "MultipleLines", "InternetService",
    "OnlineSecurity", "OnlineBackup", "DeviceProtection", "TechSupport",
    "StreamingTV", "StreamingMovies", "Contract", "PaperlessBilling",
    "PaymentMethod", "MonthlyCharges", "TotalCharges"
]

st.write("Your uploaded file should contain columns similar to these:")

st.dataframe(pd.DataFrame({"Expected Columns": expected_columns}))

st.markdown("""
Example values include:

- `gender`: Male / Female  
- `Partner`: Yes / No  
- `InternetService`: DSL / Fiber optic / No  
- `Contract`: Month-to-month / One year / Two year  
- `PaymentMethod`: Electronic check / Mailed check / Bank transfer / Credit card  
- `MonthlyCharges`: numeric value  
- `TotalCharges`: numeric value  

The file may include `Churn`, but it is not required for prediction.
""")

threshold = st.sidebar.slider(
    "Churn Risk Threshold",
    min_value=0.20,
    max_value=0.80,
    value=0.45,
    step=0.05
)

uploaded_file = st.file_uploader("Upload customer CSV file", type=["csv"])

if uploaded_file is not None:
    df_input = pd.read_csv(uploaded_file)

    st.subheader("Uploaded Data Preview")
    st.dataframe(df_input.head())

    missing_cols = [col for col in expected_columns if col not in df_input.columns]

    if missing_cols:
        st.warning(
            "Your file is missing some expected columns. "
            "The app will still try to run, but predictions may be less reliable."
        )
        st.write("Missing columns:", missing_cols)

    try:
        model = joblib.load("models/churn_model.pkl")
        features = joblib.load("models/model_features.pkl")

        df_processed = prepare_data(df_input)
        X = df_processed.reindex(columns=features, fill_value=0)

        probabilities = model.predict_proba(X)[:, 1]
        predictions = (probabilities > threshold).astype(int)

        results = df_input.copy()
        results["Churn_Prediction"] = predictions
        results["Churn_Probability"] = probabilities

        st.subheader("Prediction Results")
        st.dataframe(results)

        churn_count = int(results["Churn_Prediction"].sum())
        total_customers = len(results)
        churn_rate = (churn_count / total_customers) * 100 if total_customers > 0 else 0

        col1, col2, col3 = st.columns(3)
        col1.metric("Total Customers", total_customers)
        col2.metric("Predicted Churners", churn_count)
        col3.metric("Predicted Churn Rate", f"{churn_rate:.2f}%")

        high_risk = results[results["Churn_Prediction"] == 1]

        st.subheader("High-Risk Customers")
        st.write("Customers predicted as likely to churn based on the selected threshold.")
        st.dataframe(high_risk.head(20))

        importance = pd.Series(model.feature_importances_, index=features)
        top_features = importance.sort_values(ascending=False).head(10)

        st.subheader("Top Factors Driving Churn")
        st.bar_chart(top_features)

        csv = results.to_csv(index=False).encode("utf-8")

        st.download_button(
            label="Download Predictions",
            data=csv,
            file_name="churn_predictions.csv",
            mime="text/csv"
        )

    except Exception as e:
        st.error("Something went wrong while generating predictions.")
        st.write(e)

else:
    st.info("Upload a CSV file to begin.")