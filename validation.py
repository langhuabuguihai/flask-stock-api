import yfinance as yf
import pandas as pd

def is_valid_ticker(ticker):
    """
    Checks if the given ticker is valid on Yahoo Finance.
    """
    try:
        stock = yf.Ticker(ticker)
        # Attempt to fetch historical data; if empty, the ticker is invalid
        hist = stock.history(period="max")
        if hist.empty:
            return False
        return True
    except Exception as e:
        print(f"Error for ticker {ticker}: {e}")
        return False

def main():
    # Load data from Excel file
    try:
        # Read the Excel file and specify the starting column
        df = pd.read_excel("malaysia_stocks.xlsx", usecols="B", skiprows=1, dtype=str)  # Ensure stock codes are read as strings
        tickers = df.iloc[:, 0].dropna().tolist()  # Convert column C to a list, drop NaN values
    except Exception as e:
        print(f"Error loading Excel file: {e}")
        return

    # Check each ticker
    results = []
    for ticker in tickers:
        ticker_with_kl = f"{ticker}.KL"
        is_valid = is_valid_ticker(ticker_with_kl)
        results.append((ticker_with_kl, "Valid" if is_valid else "Invalid"))

    # Create a DataFrame with the results
    result_df = pd.DataFrame(results, columns=["Ticker", "Status"])

    # Save the results to a new Excel file
    result_df.to_excel("validated_tickers.xlsx", index=False)
    print("Validation results saved to 'validated_tickers.xlsx'.")

if __name__ == "__main__":
    main()
