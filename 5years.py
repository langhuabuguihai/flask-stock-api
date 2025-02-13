import yfinance as yf
import pandas as pd

# Define the stock ticker
ticker_symbol = "3689.KL"  # Replace with the company's ticker symbol (e.g., MSFT for Microsoft)

# Fetch the Ticker object
ticker = yf.Ticker(ticker_symbol)

# Retrieve financial data
financials = ticker.financials          # Income Statement
balance_sheet = ticker.balance_sheet    # Balance Sheet
cash_flow = ticker.cashflow             # Cash Flow Statement

# Define the output Excel file
output_file = "company_financial_reports.xlsx"

# Save the data to an Excel file with multiple sheets
with pd.ExcelWriter(output_file, engine="openpyxl") as writer:
    financials.to_excel(writer, sheet_name="Income Statement")
    balance_sheet.to_excel(writer, sheet_name="Balance Sheet")
    cash_flow.to_excel(writer, sheet_name="Cash Flow Statement")

print(f"Financial reports saved to {output_file}")
