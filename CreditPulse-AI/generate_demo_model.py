import os
import joblib
import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import LabelEncoder, StandardScaler

def generate_demo_artifacts():
    print("Generating demo machine learning dataset and preprocessor artifacts...")
    np.random.seed(42)
    n_samples = 1000

    # Define features
    data = {
        'Age': np.random.randint(18, 70, size=n_samples),
        'Annual_Income': np.random.uniform(10000, 150000, size=n_samples),
        'Monthly_Inhand_Salary': np.random.uniform(1000, 12000, size=n_samples),
        'Num_Bank_Accounts': np.random.randint(0, 10, size=n_samples),
        'Num_Credit_Cards': np.random.randint(0, 12, size=n_samples),
        'Interest_Rate': np.random.uniform(1, 35, size=n_samples),
        'Num_of_Loan': np.random.randint(0, 10, size=n_samples),
        'Delay_from_due_date': np.random.randint(0, 60, size=n_samples),
        'Num_of_Delayed_Payment': np.random.randint(0, 30, size=n_samples),
        'Changed_Credit_Limit': np.random.uniform(0, 30, size=n_samples),
        'Num_Credit_Inquiries': np.random.randint(0, 20, size=n_samples),
        'Credit_Mix': np.random.choice(['Bad', 'Standard', 'Good'], size=n_samples, p=[0.3, 0.5, 0.2]),
        'Outstanding_Debt': np.random.uniform(0, 5000, size=n_samples),
        'Credit_Utilization_Ratio': np.random.uniform(20.0, 50.0, size=n_samples),
        'Credit_History_Age_Months': np.random.randint(1, 400, size=n_samples),
        'Payment_of_Min_Amount': np.random.choice(['No', 'Yes', 'NM'], size=n_samples, p=[0.4, 0.5, 0.1]),
        'Total_EMI_per_month': np.random.uniform(0, 2000, size=n_samples),
        'Amount_invested_monthly': np.random.uniform(0, 1000, size=n_samples),
        'Payment_Behaviour': np.random.choice([
            'Low_spent_Small_value_payments',
            'High_spent_Small_value_payments',
            'Low_spent_Medium_value_payments',
            'High_spent_Medium_value_payments',
            'Low_spent_Large_value_payments',
            'High_spent_Large_value_payments'
        ], size=n_samples),
        'Monthly_Balance': np.random.uniform(0, 2000, size=n_samples)
    }

    df = pd.DataFrame(data)

    # Synthesize target variable based on financial features
    score_points = (
        (df['Annual_Income'] / 10000) * 2 +
        (df['Monthly_Balance'] / 200) * 2 +
        (df['Credit_Mix'] == 'Good') * 10 +
        (df['Credit_Mix'] == 'Standard') * 5 -
        df['Delay_from_due_date'] * 0.3 -
        df['Num_of_Delayed_Payment'] * 0.4 -
        (df['Outstanding_Debt'] / 300)
    )

    conditions = [
        score_points >= 15,
        (score_points >= 5) & (score_points < 15),
        score_points < 5
    ]
    choices = ['Good', 'Standard', 'Poor']
    df['Credit_Score'] = np.select(conditions, choices, default='Standard')

    # Categorical encoders dictionary
    categorical_cols = ['Credit_Mix', 'Payment_of_Min_Amount', 'Payment_Behaviour']
    feature_encoders = {}
    
    X = df.drop(columns=['Credit_Score']).copy()
    for col in categorical_cols:
        le = LabelEncoder()
        X[col] = le.fit_transform(X[col])
        feature_encoders[col] = le

    # Label encoder for target
    target_encoder = LabelEncoder()
    y = target_encoder.fit_transform(df['Credit_Score'])

    # Scaler
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)

    # Model
    model = RandomForestClassifier(n_estimators=100, random_state=42)
    model.fit(X_scaled, y)

    # Save artifacts
    base_dir = os.path.dirname(os.path.abspath(__file__))
    joblib.dump(model, os.path.join(base_dir, 'Credit_Scoring_Model.pkl'))
    joblib.dump(scaler, os.path.join(base_dir, 'scaler.pkl'))
    joblib.dump(target_encoder, os.path.join(base_dir, 'label_encoder.pkl'))
    joblib.dump(feature_encoders, os.path.join(base_dir, 'feature_encoders.pkl'))

    print("Artifacts successfully generated and saved:")
    print(" - Credit_Scoring_Model.pkl")
    print(" - scaler.pkl")
    print(" - label_encoder.pkl")
    print(" - feature_encoders.pkl")

if __name__ == '__main__':
    generate_demo_artifacts()
