import yfinance as yf
import pandas as pd

# Fetch data for a Malaysian stock
stock = yf.Ticker("5250.KL")

# Retrieve the cash flow data
cash_flow = stock.cashflow

# Convert the cash flow to a DataFrame (transpose for better formatting)
cash_flow_df = cash_flow.transpose()

# Save the DataFrame to an Excel file
output_file = "cash_flow.xlsx"
cash_flow_df.to_excel(output_file, sheet_name="Cash Flow")

print(f"Cash flow data saved to {output_file}")
