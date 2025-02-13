import yfinance as yf
import pandas as pd

def extract_financial_data(ticker_symbol):
    # Fetch the Ticker object
    ticker = yf.Ticker(ticker_symbol)
    
    # Extract financial reports
    balance_sheet = ticker.balance_sheet
    cash_flow = ticker.cashflow
    financials = ticker.financials
    dividends = ticker.dividends
    income_statement = ticker.financials
    
    # Initialize a dictionary to store the extracted data
    extracted_data = {}
    
    # 1. Stockholders Equity from Balance Sheet (Last 5 Years)
    extracted_data['Stockholders Equity'] = balance_sheet.loc['Total Stockholder Equity'][:5].to_dict()

    # 2. Operating Cash Flow from Cash Flow (Last 5 Years)
    extracted_data['Operating Cash Flow'] = cash_flow.loc['Total Cash From Operating Activities'][:5].to_dict()

    # 3. Net Income Continuous Operations for 5 Years from Financials
    extracted_data['Net Income Continuous Operations'] = financials.loc['Net Income From Continuing Ops'][:5].to_dict()

    # 4. The Latest Year of Dividend Distributed
    if not dividends.empty:
        latest_dividend_year = dividends.index[-1].year
        extracted_data['Latest Dividend Year'] = latest_dividend_year
        extracted_data['Latest Dividend Value'] = dividends[-1]
    else:
        extracted_data['Latest Dividend Year'] = None
        extracted_data['Latest Dividend Value'] = None

    # 5. Total Revenue from Income Statement (Last 5 Years)
    extracted_data['Total Revenue'] = income_statement.loc['Total Revenue'][:5].to_dict()

    return extracted_data

# Example usage
ticker_symbol = "AAPL"  # Replace with the stock ticker symbol of your choice
data = extract_financial_data(ticker_symbol)

# Save the extracted data to an Excel file
output_file = f"{ticker_symbol}_financial_data.xlsx"
with pd.ExcelWriter(output_file, engine="openpyxl") as writer:
    for key, value in data.items():
        pd.DataFrame(value.items(), columns=["Year", key]).to_excel(writer, sheet_name=key, index=False)

print(f"Financial data for {ticker_symbol} saved to {output_file}")
