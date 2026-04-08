from flask import Flask, request, jsonify
from flask_cors import CORS
import pickle
import numpy as np
import pandas as pd

#Initialize flask app
app = Flask(__name__)
CORS(app, origins=[
    'http://localhost:8080',
    'https://aidi-1003-final-project.vercel.app'
])

with open("cyber_threat_model_vFinal.pkl", "rb") as file:
    payload = pickle.load(file)

    model = payload["full_pipeline"]
    preprocessor = payload["preprocessor"]
    threshold = payload["threshold"]

#Feature engineering
def feature_engineering(df):

    #Time and date features
    df['timestamp'] = pd.to_datetime(df['timestamp'])
    df['hour'] = df['timestamp'].dt.hour
    df['day_of_week'] = df['timestamp'].dt.dayofweek
    df['month'] = df['timestamp'].dt.month
    df['is_weekend'] = df['timestamp'].dt.dayofweek.isin([5, 6]).astype(int)

    df.drop(columns=['timestamp'], inplace=True)

    #Apply log to bytes
    df['log_bytes_sent'] = np.log1p(df['bytes_sent'])
    df['log_bytes_received'] = np.log1p(df['bytes_received'])

    #Port binning
    bins = [-1, 1023, 49151, 65535]
    labels = ['System', 'Registered', 'Dynamic']

    df['dst_port_category'] = pd.cut(df['dst_port'], bins=bins, labels=labels)
    df['src_port_category'] = pd.cut(df['src_port'], bins=bins, labels=labels)

    #User agent
    df['user_agent'] = df['user_agent'].str.lower()
    bot_agents = ['sqlmap', 'python', 'curl', 'zgrab']
    df['riskAgent'] = df['user_agent'].apply(lambda x: 1 if any (pattern in str(x) for pattern in bot_agents) else 0)

    # Binary encode is_internal_traffic
    df['is_internal_traffic'] = df['is_internal_traffic'].astype(int)

    df.drop(columns=['url', 'src_ip', 'dst_ip'], inplace=True, errors='ignore')

    return df


#Route to check server status
@app.route("/", methods=["GET"])

def home():
    return "Server running!"

#Define prediction endpoint
@app.route("/predict", methods=["POST"])

def predict():
    try:
        data = request.get_json()

        df_raw = pd.DataFrame([data])
        df_processed = feature_engineering(df_raw)
        X_final = preprocessor.transform(df_processed)

        prob = model.predict_proba(X_final)[:, 1][0]
        prediction = 1 if prob >= threshold else 0

        return jsonify({
            "is_attack":int(prediction),
            "probability":round(float(prob), 4)

        })
    except Exception as e:
        return jsonify({
            "error": str(e), 
            "status": "failed"
        }), 400

if __name__ == "__main__":
    app.run(debug=False, host="0.0.0.0", port=5000)