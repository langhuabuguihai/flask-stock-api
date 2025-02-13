import pandas as pd
from pymongo import MongoClient

# Step 1: Connect to MongoDB
client = MongoClient("mongodb://localhost:27017/")  # Change if using MongoDB Atlas
db = client["finance_db"]  # Database name
collection = db["malaysia_stocks"]  # Collection name

# Step 2: Read the Excel file
file_path = "malaysia_stocks.xlsx"  # Path to your Excel file
df = pd.read_excel(file_path)

# Step 3: Convert DataFrame to a dictionary
# Ensure column names are strings
df.columns = [str(col) for col in df.columns]
data_dict = df.to_dict("records")

# Step 4: Insert the data into MongoDB
collection.insert_many(data_dict)
print("Data inserted into MongoDB successfully!")

# Step 5: Query and Verify
for doc in collection.find().limit(5):  # Display first 5 records
    print(doc)

count = collection.count_documents({})
print(f"Total documents in the collection: {count}")
