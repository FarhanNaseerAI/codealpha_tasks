import os
import joblib
import numpy as np
import pandas as pd
from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

# Base directory for artifacts
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

MODEL_PATH = os.path.join(BASE_DIR, 'Credit_Scoring_Model.pkl')
SCALER_PATH = os.path.join(BASE_DIR, 'scaler.pkl')
LABEL_ENCODER_PATH = os.path.join(BASE_DIR, 'label_encoder.pkl')
FEATURE_ENCODERS_PATH = os.path.join(BASE_DIR, 'feature_encoders.pkl')

model = None
scaler = None
label_encoder = None
feature_encoders = None

FEATURE_NAMES = [
    'Age', 'Annual_Income', 'Monthly_Inhand_Salary', 'Num_Bank_Accounts',
    'Num_Credit_Cards', 'Interest_Rate', 'Num_of_Loan', 'Delay_from_due_date',
    'Num_of_Delayed_Payment', 'Changed_Credit_Limit', 'Num_Credit_Inquiries',
    'Credit_Mix', 'Outstanding_Debt', 'Credit_Utilization_Ratio',
    'Credit_History_Age_Months', 'Payment_of_Min_Amount', 'Total_EMI_per_month',
    'Amount_invested_monthly', 'Payment_Behaviour', 'Monthly_Balance'
]

CATEGORICAL_COLS = ['Credit_Mix', 'Payment_of_Min_Amount', 'Payment_Behaviour']

def load_artifacts():
    """Load model and preprocessing artifacts with joblib."""
    global model, scaler, label_encoder, feature_encoders, FEATURE_NAMES, CATEGORICAL_COLS
    try:
        if os.path.exists(MODEL_PATH):
            model = joblib.load(MODEL_PATH)
        if os.path.exists(SCALER_PATH):
            scaler = joblib.load(SCALER_PATH)
            if hasattr(scaler, 'feature_names_in_'):
                FEATURE_NAMES = list(scaler.feature_names_in_)
        if os.path.exists(LABEL_ENCODER_PATH):
            label_encoder = joblib.load(LABEL_ENCODER_PATH)
        if os.path.exists(FEATURE_ENCODERS_PATH):
            feature_encoders = joblib.load(FEATURE_ENCODERS_PATH)
            if isinstance(feature_encoders, dict):
                CATEGORICAL_COLS = list(feature_encoders.keys())
    except Exception as e:
        print(f"Error loading model artifacts: {e}")

# Initial load
load_artifacts()


RECOMMENDATIONS = {
    'Good': {
        'risk_level': 'Low Financial Risk',
        'badge_class': 'bg-success-gradient',
        'status_color': 'success',
        'icon': 'fa-shield-check',
        'items': [
            'Eligible for premium loan rates & higher credit lines',
            'Strong repayment profile and solid credit foundation',
            'Low financial risk with excellent credit utilization'
        ]
    },
    'Standard': {
        'risk_level': 'Moderate Financial Risk',
        'badge_class': 'bg-warning-gradient',
        'status_color': 'warning',
        'icon': 'fa-triangle-exclamation',
        'items': [
            'Moderate financial profile with potential for growth',
            'Improve payment consistency to boost credit tier',
            'Reduce outstanding debt balances to optimize credit score'
        ]
    },
    'Poor': {
        'risk_level': 'High Financial Risk',
        'badge_class': 'bg-danger-gradient',
        'status_color': 'danger',
        'icon': 'fa-circle-xmark',
        'items': [
            'High financial risk detected in current profile',
            'Reduce outstanding debt to improve your overall credit profile.',
            'Avoid delayed payments and clear delinquent loans',
            'Increase your monthly savings to improve financial stability.'
        ]
    }
}

@app.route('/', methods=['GET'])
def index():
    """Render customer information entry form."""
    return render_template('index.html')

def format_customer_profile(form_data):
    """Format submitted form data into structured display groups with formatted values."""
    def fmt_currency(val):
        try:
            f = float(val)
            if f.is_integer():
                return f"-${abs(int(f)):,}" if f < 0 else f"${int(f):,}"
            return f"-${abs(f):,.2f}" if f < 0 else f"${f:,.2f}"
        except (ValueError, TypeError):
            return str(val)

    def fmt_number(val):
        try:
            f = float(val)
            return str(int(f)) if f.is_integer() else str(f)
        except (ValueError, TypeError):
            return str(val)

    def fmt_percent(val):
        try:
            f = float(val)
            return f"{int(f)}%" if f.is_integer() else f"{f:.1f}%"
        except (ValueError, TypeError):
            return str(val)

    def fmt_days(val):
        try:
            i = int(float(val))
            return f"{i} Day" if i == 1 else f"{i} Days"
        except (ValueError, TypeError):
            return str(val)

    def fmt_months(val):
        try:
            i = int(float(val))
            return f"{i} Month" if i == 1 else f"{i} Months"
        except (ValueError, TypeError):
            return str(val)

    def fmt_years(val):
        try:
            i = int(float(val))
            return f"{i} Years"
        except (ValueError, TypeError):
            return str(val)

    def fmt_payment_behaviour(val):
        behaviour_map = {
            'High_spent_Large_value_payments': 'High Spending • Large Value Payments',
            'High_spent_Medium_value_payments': 'High Spending • Medium Value Payments',
            'High_spent_Small_value_payments': 'High Spending • Small Value Payments',
            'Low_spent_Large_value_payments': 'Low Spending • Large Value Payments',
            'Low_spent_Medium_value_payments': 'Low Spending • Medium Value Payments',
            'Low_spent_Small_value_payments': 'Low Spending • Small Value Payments',
        }
        return behaviour_map.get(str(val), str(val).replace('_', ' '))

    def fmt_min_payment(val):
        s_val = str(val)
        if s_val == 'NM':
            return 'Not Mentioned (NM)'
        return s_val

    return [
        {
            'title': 'Personal Profile',
            'icon': 'fa-user-gear',
            'fields': [
                {'label': 'Age', 'value': fmt_years(form_data.get('Age', ''))},
                {'label': 'Annual Income', 'value': fmt_currency(form_data.get('Annual_Income', ''))},
                {'label': 'Monthly Salary', 'value': fmt_currency(form_data.get('Monthly_Inhand_Salary', ''))},
                {'label': 'Active Bank Accounts', 'value': fmt_number(form_data.get('Num_Bank_Accounts', ''))},
                {'label': 'Monthly Investment', 'value': fmt_currency(form_data.get('Amount_invested_monthly', ''))},
                {'label': 'Remaining Monthly Balance', 'value': fmt_currency(form_data.get('Monthly_Balance', ''))},
            ]
        },
        {
            'title': 'Credit & Liabilities',
            'icon': 'fa-credit-card',
            'fields': [
                {'label': 'Active Credit Cards', 'value': fmt_number(form_data.get('Num_Credit_Cards', ''))},
                {'label': 'Interest Rate', 'value': fmt_percent(form_data.get('Interest_Rate', ''))},
                {'label': 'Number of Loans', 'value': fmt_number(form_data.get('Num_of_Loan', ''))},
                {'label': 'Outstanding Debt', 'value': fmt_currency(form_data.get('Outstanding_Debt', ''))},
                {'label': 'Credit Utilization', 'value': fmt_percent(form_data.get('Credit_Utilization_Ratio', ''))},
                {'label': 'Monthly EMI', 'value': fmt_currency(form_data.get('Total_EMI_per_month', ''))},
            ]
        },
        {
            'title': 'Repayment Behaviour',
            'icon': 'fa-clock-rotate-left',
            'fields': [
                {'label': 'Delay from Due Date', 'value': fmt_days(form_data.get('Delay_from_due_date', ''))},
                {'label': 'Delayed Payments', 'value': fmt_number(form_data.get('Num_of_Delayed_Payment', ''))},
                {'label': 'Changed Credit Limit', 'value': fmt_percent(form_data.get('Changed_Credit_Limit', ''))},
                {'label': 'Credit Inquiries', 'value': fmt_number(form_data.get('Num_Credit_Inquiries', ''))},
                {'label': 'Credit History', 'value': fmt_months(form_data.get('Credit_History_Age_Months', ''))},
                {'label': 'Credit Mix', 'value': str(form_data.get('Credit_Mix', ''))},
                {'label': 'Minimum Payment', 'value': fmt_min_payment(form_data.get('Payment_of_Min_Amount', ''))},
                {'label': 'Payment Behaviour', 'value': fmt_payment_behaviour(form_data.get('Payment_Behaviour', ''))},
            ]
        }
    ]

@app.route('/predict', methods=['POST'])
def predict():
    """Handle model inference with complete input validation and exception handling."""
    # Ensure artifacts are loaded
    if model is None or scaler is None or label_encoder is None or feature_encoders is None:
        load_artifacts()
        if model is None or scaler is None or label_encoder is None or feature_encoders is None:
            return render_template(
                'index.html',
                error_message="Model artifacts not found. Please ensure .pkl files are placed in the application root directory."
            )

    try:
        form_data = request.form
        processed_data = {}

        # 1. Parse and validate numerical inputs
        numerical_fields = {
            'Age': (18, 120, int),
            'Annual_Income': (0, 10000000, float),
            'Monthly_Inhand_Salary': (0, 1000000, float),
            'Num_Bank_Accounts': (0, 50, int),
            'Num_Credit_Cards': (0, 50, int),
            'Interest_Rate': (0, 100, float),
            'Num_of_Loan': (0, 50, int),
            'Delay_from_due_date': (0, 365, int),
            'Num_of_Delayed_Payment': (0, 365, int),
            'Changed_Credit_Limit': (-100, 1000, float),
            'Num_Credit_Inquiries': (0, 100, int),
            'Outstanding_Debt': (0, 1000000, float),
            'Credit_Utilization_Ratio': (0, 100, float),
            'Credit_History_Age_Months': (0, 1200, int),
            'Total_EMI_per_month': (0, 1000000, float),
            'Amount_invested_monthly': (0, 1000000, float),
            'Monthly_Balance': (-10000, 1000000, float)
        }

        for field, (min_val, max_val, cast_type) in numerical_fields.items():
            raw_val = form_data.get(field)
            if raw_val is None or raw_val.strip() == '':
                return render_template('index.html', error_message=f"Missing required field: {field.replace('_', ' ')}")
            
            try:
                val = cast_type(raw_val)
                if val < min_val or val > max_val:
                    return render_template(
                        'index.html',
                        error_message=f"{field.replace('_', ' ')} must be between {min_val} and {max_val}."
                    )
                processed_data[field] = val
            except ValueError:
                return render_template('index.html', error_message=f"Invalid numeric input for {field.replace('_', ' ')}")

        # 2. Parse and encode categorical inputs
        for col in CATEGORICAL_COLS:
            val = form_data.get(col)
            if not val:
                return render_template('index.html', error_message=f"Please select a valid option for {col.replace('_', ' ')}")
            
            encoder = feature_encoders.get(col)
            if encoder is not None:
                try:
                    # Transform categorical feature
                    encoded_val = encoder.transform([val])[0]
                    processed_data[col] = encoded_val
                except Exception:
                    # Fallback for unexpected label
                    processed_data[col] = 0
            else:
                processed_data[col] = 0

        # 3. Create DataFrame with exact column ordering
        for col in FEATURE_NAMES:
            if col not in processed_data:
                processed_data[col] = 0

        input_df = pd.DataFrame([processed_data])[FEATURE_NAMES]

        # 4. Scale feature matrix
        scaled_input = scaler.transform(input_df)

        # 5. Predict class and probabilities
        prediction_id = model.predict(scaled_input)[0]

        # Calculate prediction confidence
        confidence = 0.0
        if hasattr(model, 'predict_proba'):
            proba = model.predict_proba(scaled_input)[0]
            confidence = float(np.max(proba) * 100)
        else:
            confidence = 85.0  # Fallback standard confidence

        # 6. Decode prediction label using LabelEncoder
        if hasattr(label_encoder, 'inverse_transform'):
            predicted_label = str(label_encoder.inverse_transform([prediction_id])[0])
        else:
            label_map = {0: 'Poor', 1: 'Standard', 2: 'Good'}
            predicted_label = label_map.get(prediction_id, 'Standard')

        # Format details
        rec_details = RECOMMENDATIONS.get(predicted_label, RECOMMENDATIONS['Standard'])


        return render_template(
            'result.html',
            predicted_score=predicted_label,
            confidence=round(confidence, 1),
            risk_level=rec_details['risk_level'],
            badge_class=rec_details['badge_class'],
            status_color=rec_details['status_color'],
            icon=rec_details['icon'],
            recommendations=rec_details['items'],
            input_summary={k.replace('_', ' '): v for k, v in form_data.items()},
            profile_groups=format_customer_profile(form_data)
        )

    except Exception as e:
        print(f"Prediction Error: {e}")
        return render_template(
            'index.html',
            error_message=f"An error occurred during prediction analysis: {str(e)}"
        )

@app.route('/health', methods=['GET'])
def health():
    """Health check endpoint."""
    artifacts_status = {
        'model_loaded': model is not None,
        'scaler_loaded': scaler is not None,
        'label_encoder_loaded': label_encoder is not None,
        'feature_encoders_loaded': feature_encoders is not None
    }
    return jsonify({'status': 'online', 'artifacts': artifacts_status})

if __name__ == '__main__':
    # Run development server
    app.run(host='0.0.0.0', port=5000, debug=True)
