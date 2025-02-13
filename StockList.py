from pymongo import MongoClient
import pandas as pd

# Load the Excel file
file_path = r"C:\Users\JEE JIA BIN\Downloads\FYP Data\Excel_File\malaysia_stocks.xlsx"
sheet_name = 'Table 2'
data = pd.read_excel(file_path, sheet_name=sheet_name)

# Connect to MongoDB
client = MongoClient("mongodb://localhost:27017/")  # Replace with your MongoDB URI
db = client["StockData"]  # Create/use database named "StockData"
collection = db["MalaysiaStocks"]  # Create/use collection named "MalaysiaStocks"

# Convert DataFrame to dictionary and insert into MongoDB
data_dict = data.to_dict("records")
collection.insert_many(data_dict)

print("Data successfully stored in MongoDB!")
