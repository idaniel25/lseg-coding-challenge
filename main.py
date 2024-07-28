import os
import requests
import pandas as pd
import json

BASE_URL = "http://127.0.0.1:5000"


def process_files(files_number):
    """
    Processes the specified number of files for each stock exchange
    """
    base_directory = "stock_price_data_files"
    stock_exchange_directories = [d for d in os.listdir(base_directory) if os.path.isdir(os.path.join(base_directory, d))]

    for stock_exchange_dir in stock_exchange_directories:
        directory = os.path.join(base_directory, stock_exchange_dir)
        files = get_files(directory, files_number)
        predictions_dir = create_predictions_dir(directory)

        for file in files:
            file_path = os.path.join(directory, file)
            extracted_data = extract_data(file_path)
            if extracted_data is None:
                continue

            predictions = predict_data(extracted_data)
            if predictions is None:
                continue

            output_file = os.path.join(predictions_dir, f"predicted_{file}")
            save_predictions(output_file, predictions)


def save_predictions(output_file, predictions):
    predictions.to_csv(output_file, header=False, index=False)
    print(f"Predictions saved to {output_file}")


def predict_data(extracted_data):
    """Send a request to the /predict endpoint to predict the next three data points"""
    response = requests.post(f"{BASE_URL}/predict", json=extracted_data.to_dict(orient="records"))
    if response.status_code != 200:
        print(f"Prediction error: {response.json()['error']}")
        return None
    response_list = response.json()
    response_json = json.dumps(response_list)
    predictions = pd.read_json(response_json, orient="records")
    predictions = format_predictions(predictions)
    print(predictions)
    return predictions


def format_predictions(predictions):
    """Format the price column to have two decimals"""
    predictions[2] = predictions[2].apply(lambda x: f"{x:.2f}")
    return predictions


def extract_data(file_path):
    """Send a request to the /extract endpoint to extract data from a stock file"""
    response = requests.post(f"{BASE_URL}/extract", json={"file_path": file_path})
    if response.status_code != 200:
        print(f"Error extracting data from {file_path}: {response.json()['error']}")
        return None
    response_list = response.json()
    response_json = json.dumps(response_list)
    return pd.read_json(response_json, orient="records")


def create_predictions_dir(directory):
    predictions_dir = os.path.join(directory, 'predictions')
    if not os.path.exists(predictions_dir):
        os.makedirs(predictions_dir)
    return predictions_dir


def get_files(directory, files_number):
    try:
        files = [f for f in os.listdir(directory) if f.endswith('.csv')]
        return files[:files_number]
    except Exception as e:
        print(f"Error getting files from {directory}: {e}")
        return None


if __name__ == "__main__":
    no_files = 2
    process_files(no_files)
