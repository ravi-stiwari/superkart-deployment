from flask import Flask, request, jsonify
import joblib
import pandas as pd
import numpy as np
import os

app = Flask(__name__)

# Load the serialized model
model = joblib.load("superkart_model.pkl")

@app.route("/", methods=["GET"])
def home():
    return jsonify({
        "message": "SuperKart Sales Prediction API",
        "status": "running",
        "endpoints": {
            "/predict": "POST - Single prediction",
            "/predict_batch": "POST - Batch prediction (CSV file)"
        }
    })

@app.route("/predict", methods=["POST"])
def predict():
    try:
        data = request.get_json()

        # Create DataFrame from input
        input_df = pd.DataFrame([data])

        # Make prediction
        prediction = model.predict(input_df)

        return jsonify({
            "prediction": round(float(prediction[0]), 2),
            "status": "success"
        })
    except Exception as e:
        return jsonify({
            "error": str(e),
            "status": "error"
        }), 400

@app.route("/predict_batch", methods=["POST"])
def predict_batch():
    try:
        file = request.files["file"]
        input_df = pd.read_csv(file)

        # Make predictions
        predictions = model.predict(input_df)

        # Add predictions to the dataframe
        input_df["Predicted_Sales"] = np.round(predictions, 2)

        return jsonify({
            "predictions": input_df.to_dict(orient="records"),
            "count": len(predictions),
            "status": "success"
        })
    except Exception as e:
        return jsonify({
            "error": str(e),
            "status": "error"
        }), 400

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=7860)
