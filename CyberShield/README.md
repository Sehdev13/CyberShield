# CyberShield — Network Threat Detection

A machine learning web app that analyzes network traffic records and flags potential cyberattacks, complete with a confidence score.

---

## Live Demo

[CyberShield Live Here!](https://aidi-1003-final-project.vercel.app/)

---

## Project Overview

You send it a network traffic record (ports, bytes, user agent, etc.) and it tells you whether it looks like an attack or not, along with a confidence score.

The dataset is heavily imbalanced (96% benign, 4% attack), so accuracy alone is useless as a metric. Three models were trained and compared using F1 score on the attack class, with 5-fold stratified cross-validation via GridSearchCV:

| Model | F1 (attack class) |
|---|---|
| Logistic Regression | 0.23 |
| Random Forest | 0.39 |
| **XGBoost** | **0.63** |

XGBoost won. LR and RF used SMOTE + `class_weight='balanced'` to handle imbalance. XGBoost used `scale_pos_weight`.

---

## Project Structure

```
├── Backend/
│   ├── app.py                          # Flask REST API
│   ├── cyber_threat_model_vFinal.pkl   # Saved model + preprocessor + threshold
│   └── requirements.txt
├── Frontend/
│   └── index.html                      # Single-page UI
└── Notebooks - dataset/
    ├── Final_Project_(Supervised)_AIDI1003.ipynb   # EDA, training, evaluation
    └── cybersecurity.csv               # Dataset
```

---

## API

Send a POST request to `/predict`:

**Request:**
```json
{
  "timestamp": "2025-10-01 00:12:54",
  "src_ip": "192.168.1.1",
  "dst_ip": "10.0.0.1",
  "src_port": 56377,
  "dst_port": 445,
  "protocol": "TCP",
  "bytes_sent": 8029,
  "bytes_received": 17204,
  "user_agent": "Mozilla/5.0 ...",
  "url": "https://example.com",
  "is_internal_traffic": false
}
```

**Response:**
```json
{
  "is_attack": 1,
  "probability": 0.8741
}
```

---

## Running Locally

**Backend:**
```bash
cd Backend
pip install -r requirements.txt
python app.py
```

**Frontend:**
Just open `Frontend/index.html` in a browser, or serve it with any static server.

---

## Tech Stack

- **Model:** XGBoost, scikit-learn, pandas, numpy
- **API:** Flask + Flask-CORS
- **Frontend:** Vanilla HTML/CSS/JS
- **Deployment:** Vercel (frontend) + Render (backend)

---

## Dependencies

```
flask
flask-cors
numpy
pandas
scikit-learn
xgboost
gunicorn
```
