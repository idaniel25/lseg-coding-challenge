# Stock Price Prediction

This project predicts the next three stock prices based on sampled data from given CSV files.

## Setup

1. Clone the repository.
2. Install the required dependencies:
    ```
    python 3.7 or higher
    pip install pandas Flask requests
    ```
   
## Running the Application
1. **Adjust the `no_files` variable in `main.py` to specify how many files to process per stock exchange.**
2. **Run the Flask Server (app.py):**
The Flask server will start at `http://127.0.0.1:5000`.
2. **Process the files:**
Run the main.py file