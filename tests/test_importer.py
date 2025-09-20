import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.importer import DataImporter
from src.validator import DataValidator

def test_importer():
    
    # Delete old test database
    if os.path.exists("test_financial_data.db"):
        os.remove("test_financial_data.db")
    
    # Rest of your test...
    print("Testing importer...")
    importer = DataImporter("test_financial_data.db")
    validator = DataValidator()

    #create table
    importer.create_table()

    #get some transactions
    transactions = validator.parse_json("sample_data/transactions.json")
    #import transactions
    importer.import_transactions(transactions)
    #close importer
    importer.close()
    print("Importer tests completed")

def verify_import():
    print("\n=== Verifying Import ===")
    
    # Reconnect to check the data
    importer = DataImporter("test_financial_data.db")
    
    # Query the database to see what's in there
    importer.cursor.execute("SELECT COUNT(*) FROM transactions")
    count = importer.cursor.fetchone()[0]
    print(f"📊 Found {count} transactions in database")
    
    # Get first few records to verify
    importer.cursor.execute("SELECT transaction_id, amount, date, account FROM transactions LIMIT 3")
    records = importer.cursor.fetchall()
    
    print("\n📋 First 3 transactions:")
    for record in records:
        print(f"  ID: {record[0]}, Amount: ${record[1]}, Date: {record[2]}, Account: {record[3]}")
    
    importer.close()

# Add this to your test file and call it:
if __name__ == "__main__":
    test_importer()
    verify_import()
   


