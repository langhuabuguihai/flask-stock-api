import yfinance as yf
import pandas as pd
import logging

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
    data_frames["Balance Sheet"] = safe_fetch(lambda: stock.balance_sheet.transpose(), "Balance Sheet")
    data_frames["Cash Flow"] = safe_fetch(lambda: stock.cashflow.transpose(), "Cash Flow")
    data_frames["Financials"] = safe_fetch(lambda: stock.financials.transpose(), "Financials")
    data_frames["Quarterly Financials"] = safe_fetch(lambda: stock.quarterly_financials.transpose(), "Quarterly Financials")
    data_frames["Recommendations"] = safe_fetch(lambda: stock.recommendations, "Recommendations")
    data_frames["Institutional Holders"] = safe_fetch(lambda: stock.institutional_holders, "Institutional Holders")
    data_frames["Major Holders"] = safe_fetch(lambda: stock.major_holders, "Major Holders")
    data_frames["Dividends"] = safe_fetch(lambda: stock.dividends, "Dividends")
    data_frames["Splits"] = safe_fetch(lambda: stock.splits, "Splits")
    data_frames["History"] = safe_fetch(lambda: stock.history(period="max"), "History")

    # Optional: Try fetching income statement for net income as an alternative to deprecated earnings
    data_frames["Income Statement"] = safe_fetch(lambda: stock.income_stmt.transpose(), "Income Statement")

    return data_frames

def save_to_excel(data_frames, output_file):
    with pd.ExcelWriter(output_file, engine="openpyxl") as writer:
        for sheet_name, df in data_frames.items():
            if df is not None and not df.empty:
                if isinstance(df, pd.Series):
                    df = df.to_frame()

                # Handle timezone-aware datetime
                if isinstance(df.index, pd.DatetimeIndex):
                    df.index = df.index.tz_localize(None)
                if isinstance(df.columns, pd.DatetimeIndex):
                    df.columns = df.columns.tz_localize(None)

                # Write to Excel
                df.to_excel(writer, sheet_name=sheet_name)
    print(f"All data saved to {output_file}")

# Specify the stock ticker symbol
ticker_symbol = "3689.KL"

# Fetch stock data
data_frames = fetch_stock_data(ticker_symbol)

# Save to Excel
output_file = "F&N.xlsx"
save_to_excel(data_frames, output_file)
