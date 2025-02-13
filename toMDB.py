import yfinance as yf
import pandas as pd
import logging
from pymongo import MongoClient
import time


# Configure logging
logging.basicConfig(
    filename="stock_data_errors.log",
    level=logging.WARNING,
    format="%(asctime)s - %(levelname)s - %(message)s",
)

def fetch_stock_data(ticker_symbol):
    stock = yf.Ticker(ticker_symbol)
    data_frames = {}

    def safe_fetch(fetch_func, description):
        """Helper to fetch data with error handling."""
        try:
            return fetch_func()
        except Exception as e:
            logging.warning(f"Error fetching {description} for {ticker_symbol}: {e}")
            return None

    # Fetch data
    data_frames["Summary"] = safe_fetch(lambda: pd.DataFrame.from_dict(stock.info, orient="index", columns=["Value"]), "Summary")
    data_frames["BalanceSheet"] = safe_fetch(lambda: stock.balance_sheet.transpose(), "Balance Sheet")
    data_frames["CashFlow"] = safe_fetch(lambda: stock.cashflow.transpose(), "Cash Flow")
    data_frames["Financials"] = safe_fetch(lambda: stock.financials.transpose(), "Financials")
    data_frames["QuarterlyFinancials"] = safe_fetch(lambda: stock.quarterly_financials.transpose(), "Quarterly Financials")
    data_frames["Income Statement"] = safe_fetch(lambda: stock.income_stmt.transpose(), "Income Statement")
    
    return data_frames

def save_to_mongodb(data_frames, db_name, ticker_symbol):
    # Connect to MongoDB
    client = MongoClient("mongodb://localhost:27017/")  # Adjust the URI for your MongoDB server
    db = client[db_name]
    
    for collection_name, df in data_frames.items():
        if df is not None and not df.empty:
            if isinstance(df, pd.Series):
                df = df.to_frame()

            # Handle timezone-aware datetime
            if isinstance(df.index, pd.DatetimeIndex):
                df.index = df.index.tz_localize(None)
            if isinstance(df.columns, pd.DatetimeIndex):
                df.columns = df.columns.tz_localize(None)

            # Reset the index to include it in MongoDB documents
            df.reset_index(inplace=True)

            # Convert DataFrame to dictionary
            data_dict = df.to_dict("records")

            # Insert into MongoDB with ticker symbol
            collection = db[collection_name]
            for document in data_dict:
                document["ticker_symbol"] = ticker_symbol  # Add stock identifier
            collection.insert_many(data_dict)
    
    print(f"Data for {ticker_symbol} saved to MongoDB.")

def process_multiple_stocks(stock_list, db_name):
    for ticker_symbol in stock_list:
        print(f"Processing {ticker_symbol}...")
        data_frames = fetch_stock_data(ticker_symbol)
        save_to_mongodb(data_frames, db_name, ticker_symbol)

        time.sleep(5)

# Example stock list
stock_list = ["5250.KL", "3557.KL", "7167.KL", "3689.KL"]

# Process and store data for multiple stocks
db_name = "StockData"
process_multiple_stocks(stock_list, db_name)
