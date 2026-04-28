# 📉 Customer Churn Prediction App

## 🚀 Overview

This project is a machine learning-powered customer churn prediction app built with Streamlit.

It allows users to upload customer data and identify which customers are likely to churn, along with churn probability scores.

The goal is to help businesses take proactive retention actions before losing valuable customers.

---

## 🎯 Problem Statement

Customer churn is a major challenge for subscription-based businesses such as telecoms, SaaS companies, banks, and digital platforms.

This project answers:

> Which customers are most likely to leave?

---

## 🧠 What This App Does

- Upload customer CSV data
- Preprocess customer features
- Predict churn risk
- Generate churn probability scores
- Highlight high-risk customers
- Show top factors driving churn
- Download prediction results

---

## 🛠️ Tech Stack

- Python
- pandas
- scikit-learn
- Streamlit
- joblib

---

## 🤖 Machine Learning Approach

The model is trained using a Random Forest Classifier.

Key steps:

- Data cleaning
- Categorical encoding
- Feature alignment for uploaded data
- Model training
- Probability-based churn prediction
- Threshold tuning for risk sensitivity

---

## 📊 Model Performance

Baseline model performance:

- Accuracy: ~80%
- Churn recall improved using class balancing and threshold adjustment

The model is optimized to support business decision-making by identifying more at-risk customers.

---

## 📂 Expected Dataset Format

The app expects customer data similar to the Telco Customer Churn dataset.

Expected columns include:

```text
customerID
gender
SeniorCitizen
Partner
Dependents
tenure
PhoneService
MultipleLines
InternetService
OnlineSecurity
OnlineBackup
DeviceProtection
TechSupport
StreamingTV
StreamingMovies
Contract
PaperlessBilling
PaymentMethod
MonthlyCharges
TotalCharges


