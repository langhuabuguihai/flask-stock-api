import firebase_admin
from firebase_admin import credentials, firestore
import pandas as pd

# Initialize Firestore
cred = credentials.Certificate(r"c:\Users\JEE JIA BIN\AndroidStudioProjects\firstFYP\myfyp-6f913-firebase-adminsdk-p4esv-e4c08170c7.json")  # Replace with your JSON key path
firebase_admin.initialize_app(cred)
db = firestore.client()

# Load stock data
file_path = "malaysia_stocks.xlsx"  # Replace with your file path
data = pd.read_excel(file_path, sheet_name="Table 2")

# Upload data to Firestore
collection_name = "stocks"
for _, row in data.iterrows():
    doc_ref = db.collection(collection_name).document(row["Ticker"])
    doc_ref.set({
        "name": row["Name"],
        "code": row["Code"],
        
        "ticker": row["Ticker"]
    })
    print(f"Uploaded {row['Name']} to Firestore")

print("Upload complete.")
