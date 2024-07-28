import json
from flask import Flask, request, jsonify
import pandas as pd
from data_extractor import extract_data
from predictor import predict_next_three_entries

app = Flask(__name__)


@app.route('/extract', methods=['POST'])
def extract():
    try:
        data = request.json
        file_path = data['file_path']
        if not file_path:
            return jsonify({"error": "File path not provided"}), 400

        extracted_data = extract_data(file_path)
        if extracted_data is None:
            return jsonify({"error": "Error extracting data"}), 400

        if extracted_data.empty:
            return jsonify({"error": "The file is empty"}), 400

        return extracted_data.to_json(orient="records")
    except Exception as e:
        return jsonify({"error": f"An error occured: {e}"}), 500


@app.route('/predict', methods=['POST'])
def predict():
    try:
        data = request.json
        if not data:
            return jsonify({"error": "No data provided"}), 400

        extracted_data_json = json.dumps(data)
        extracted_data = pd.read_json(extracted_data_json, orient="records")
        predictions = predict_next_three_entries(extracted_data)
        if predictions is None:
            return jsonify({"error": "Prediction error"}), 400
        if predictions.empty:
            return jsonify({"error": "The prediction file is empty"}), 400

        return predictions.to_json(orient="records")
    except Exception as e:
        return jsonify({"error": f"An occured: {e}"}), 500


if __name__ == "__main__":
    app.run(debug=True)