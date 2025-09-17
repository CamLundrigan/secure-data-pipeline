import sys
import os

# Add the parent directory to Python's path so it can find the src module
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.validator import DataValidator

validator = DataValidator()

def test_parse_json():
    print("\n=== Testing JSON Data ===")
    transactions = validator.parse_json("sample_data/transactions.json")
    for i, transaction in enumerate(transactions, 1):
        errors = validator.validate_transaction(transaction)
        if errors:
            print(f"Transaction {i}: ERRORS - {errors}")
        else:
            print(f"Transaction {i}: VALID")

def test_good_csv():
    print("\n=== Testing Good CSV Data ===")
    transactions = validator.parse_csv("sample_data/good_transactions.csv")
    for i, transaction in enumerate(transactions, 1):
        errors = validator.validate_transaction(transaction)
        if errors:
            print(f"Transaction {i}: ERRORS - {errors}")
        else:
            print(f"Transaction {i}: VALID")
        
def test_bad_csv():
    print("\n=== Testing Bad CSV Data ===")
    transactions = validator.parse_csv("sample_data/bad_transactions.csv")
    for i, transaction in enumerate(transactions, 1):
        errors = validator.validate_transaction(transaction)
        if errors:
            print(f"Transaction {i}: ERRORS")
            for error in errors:
                print(f"  - {error}")
        else:
            print(f"Transaction {i}: VALID")

if __name__ == "__main__":
    test_parse_json()
    print("All tests completed for JSON")
    test_good_csv()
    print("All tests completed for CSV")
    test_bad_csv()
    print("All tests completed for CSV")