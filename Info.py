import yfinance as yf
import pandas as pd

# Fetch data for a Malaysian stock
stock = yf.Ticker("5250.KL")

# Retrieve the balance sheet
balance_sheet = stock.balance_sheet

# Convert the balance sheet to a DataFrame (transpose for better formatting)
balance_sheet_df = balance_sheet.transpose()

# Save the DataFrame to an Excel file
output_file = "balance_sheet.xlsx"
balance_sheet_df.to_excel(output_file, sheet_name="Balance Sheet")

print(f"Balance sheet saved to {output_file}")
