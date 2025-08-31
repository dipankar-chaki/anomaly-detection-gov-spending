from flask import Flask, request, jsonify
import pickle
import pandas as pd
import numpy as np
from sklearn.ensemble import IsolationForest

app = Flask(__name__)

# Train or load model
def load_model():
    # Either train fresh or load from pickle
    model = IsolationForest(contamination=0.1, random_state=42)
    # Add training logic or load from saved file
    return model

model = load_model()

@app.route('/predict', methods=['POST'])
def predict_anomaly():
    """
    Endpoint to detect anomalies in transaction data
    Input: JSON with transaction features
    Output: Anomaly score and classification
    """
    try:
        data = request.json
        # Convert to DataFrame for model input
        df = pd.DataFrame([data])
        
        # Make prediction
        anomaly_score = model.decision_function(df)[0]
        is_anomaly = model.predict(df)[0]
        
        return jsonify({
            'is_anomaly': bool(is_anomaly == -1),
            'anomaly_score': float(anomaly_score),
            'status': 'success'
        })
    except Exception as e:
        return jsonify({'error': str(e), 'status': 'failed'}), 400

@app.route('/health', methods=['GET'])
def health_check():
    return jsonify({'status': 'healthy', 'model': 'loaded'})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=False)