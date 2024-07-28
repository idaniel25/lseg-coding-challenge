import os.path
import random
import pandas as pd


def extract_data(file_path):
    """
    :param file_path:
    :return: 10 consecutive data points from a random timestamp in the file
    """
    try:
        if not os.path.isfile(file_path):
            raise FileNotFoundError(f"File not found: {file_path}")

        stock_file = pd.read_csv(file_path, header=None)

        if stock_file.empty:
            raise ValueError(f"The file is empty: {file_path}")

        if len(stock_file) < 10:
            raise ValueError("Not enough entries in the file")

        random_timestamp = random.randint(0, len(stock_file) - 10)
        extracted_data = stock_file.iloc[random_timestamp:random_timestamp + 10]
        return extracted_data
    except FileNotFoundError as fnfe:
        print(fnfe)
    except ValueError as ve:
        print(ve)
    except Exception as e:
        print(f"Error extracting data from {file_path}: {e}")
        return None

