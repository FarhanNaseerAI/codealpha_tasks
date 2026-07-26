# 💳 Credit Risk Scoring Flask Web Application

A deployment-ready, modern machine learning web application built with **Flask**, **scikit-learn**, **Bootstrap 5**, and a sleek **Glassmorphic Fintech UI**. The application consumes pre-trained machine learning model artifacts (`Credit_Scoring_Model.pkl`, `scaler.pkl`, `label_encoder.pkl`, `feature_encoders.pkl`) to evaluate customer creditworthiness, predict risk classes (**Good**, **Standard**, **Poor**), compute probability confidence scores, and deliver actionable financial recommendations.

---

## 🌟 Key Features

* 🚀 **Zero Retraining Pipeline**: Uses strictly finalized, saved `.pkl` preprocessors and model binaries.
* 🛡️ **Comprehensive Validation & Error Handling**: Robust client-side and server-side checks for numeric ranges and missing inputs.
* 📊 **Probability Confidence Meter**: Visual circular gauge displaying `predict_proba()` classification confidence percentage.
* 🎨 **Fintech Glassmorphism Interface**: Dark slate theme, ambient radial glows, responsive grid layout, and micro-animations.
* 💡 **Intelligent Recommendations**: Dynamic risk level badges and tailored recommendations based on predicted score tier:
  * 🟢 **Good (Green)**: Eligible for loans, strong repayment profile, low financial risk.
  * 🟡 **Standard (Orange/Amber)**: Moderate financial profile, payment consistency guidance, debt reduction advice.
  * 🔴 **Poor (Red)**: High financial risk, debt reduction strategy, delinquency avoidance tips, balance accumulation recommendations.
* ⚡ **Quick-Fill Demo Profiles**: 1-click test buttons (`Good`, `Standard`, `Poor`) to immediately evaluate sample customer data.

---

## 🛠️ Technology Stack

* **Backend**: Python 3.10+, Flask 3.0+, Joblib, Pandas, NumPy
* **Machine Learning**: Scikit-Learn (Random Forest / XGBoost / LightGBM Classifier)
* **Frontend**: HTML5, Vanilla CSS3 (Glassmorphism & CSS Variables), JavaScript (ES6+), Bootstrap 5.3, Font Awesome 6
* **Typography**: Google Fonts (*Outfit* & *Inter*)

---

## 📁 Directory Structure

```text
Credit-Scoring-App/
│
├── app.py                      # Flask backend entry point & ML preprocessing pipeline
├── generate_demo_model.py      # Artifact synthesizer script (for quick out-of-the-box testing)
├── requirements.txt            # Python dependencies
├── README.md                   # Project documentation & execution guide
├── Credit_Scoring_Model.pkl    # Pre-trained ML classifier model
├── scaler.pkl                  # Fitted StandardScaler / MinMaxScaler
├── label_encoder.pkl           # Fitted LabelEncoder for target score class
├── feature_encoders.pkl        # Dictionary of fitted categorical encoders
│
├── templates/
│   ├── index.html              # Customer information entry form (Fintech UI)
│   └── result.html             # Credit score assessment & intelligence dashboard
│
└── static/
    ├── css/
    │   └── style.css           # Custom glassmorphism, color variables & animations
    ├── js/
    │   └── script.js           # Form validation, loading overlay & demo quick-fillers
    └── images/                 # Image assets and favicon placeholders
```

---

## ⚡ Installation & Setup Guide

### 1. Clone or Download Repository
```bash
cd Credit-Scoring-App
```

### 2. Create & Activate Virtual Environment (Recommended)
```bash
# Windows
python -m venv venv
venv\Scripts\activate

# macOS / Linux
python3 -m venv venv
source venv/bin/activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Ensure Model Files are Present
Place your pre-trained `.pkl` files into the root directory:
- `Credit_Scoring_Model.pkl`
- `scaler.pkl`
- `label_encoder.pkl`
- `feature_encoders.pkl`

*(Note: If you don't have model files ready yet, simply run `python generate_demo_model.py` to create demo model artifacts automatically!)*

---

## 🚀 Running the Application

Start the Flask development server:
```bash
python app.py
```
Open your web browser and navigate to:
```text
http://127.0.0.1:5000
```

---

## 📸 Screenshots & UI Previews

### 1. Customer Assessment Form (`/`)
* Modern fintech layout with 3 structured input cards (Personal Profile, Credit Liabilities, Repayment History).
* Interactive Quick Demo Fillers (`Good`, `Standard`, `Poor`).
* Animated loading overlay while prediction runs.

### 2. Risk Assessment Dashboard (`/predict`)
* Adaptive score status card with distinct glowing color themes (**Good → Emerald Green**, **Standard → Warm Amber**, **Poor → Crimson Red**).
* Classification confidence meter ring.
* Strategic financial advice list and collapsible submitted audit log drawer.

---

## 🔮 Future Improvements

- [ ] PDF report generation for customer credit evaluations.
- [ ] Multi-tenant API authentication token support (`/api/v1/predict`).
- [ ] What-If Financial Simulator allowing users to see how reducing debt increases their score tier.
- [ ] Database integration (PostgreSQL / SQLite) for historical credit assessment logging.

---

## 📄 License & Attribution

Developed for **Credit Scoring Machine Learning Application**. Free for educational and commercial deployment.
