import pandas as pd
from datetime import datetime, timedelta


def predict_next_three_entries(extracted_stock_file):
    """
    :param: extracted_stock_file:
    :return: the prediction of the next three values from the extracted_stock_file parameter
    """
    try:
        stock_id = extracted_stock_file.iloc[0, 0]
        timestamps = list(extracted_stock_file.iloc[:, 1])
        prices = list(extracted_stock_file.iloc[:, 2])

        distinct_prices = set(prices)
        if len(distinct_prices) < 2:
            raise ValueError("Not enough distinct prices")

        n1 = sorted(distinct_prices)[-2]
        n2 = round(n1 + (prices[-1] - n1) / 2, 2)
        n3 = round(n2 + (n1 - n2) / 4, 2)

        next_prices = [n1, n2, n3]
        next_timestamps = generate_next_three_timestamps(timestamps[-1])

        predictions = pd.DataFrame({
            0: [stock_id] * 3,
            1: next_timestamps,
            2: next_prices
        })
        combined_df = pd.concat([extracted_stock_file, predictions], ignore_index=True)
        return combined_df
    except Exception as e:
        print(f"Prediction error: {e}")
        return None


def generate_next_three_timestamps(last_timestamp):
    """
    :param: last_timestamp:
    :return: the next three timestamps after {last_timestamp}.
    """
    try:
        last_date = datetime.strptime(last_timestamp, "%d-%m-%Y")
        next_timestamps = [(last_date + timedelta(days=i)).strftime("%d-%m-%Y") for i in range(1, 4)]
        return next_timestamps
    except Exception as e:
        print(f"Error generating next timestamps: {e}")
        return None
