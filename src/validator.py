import json
import xml.etree.ElementTree as ET
import csv
from datetime import datetime

class DataValidator:
    def __init__(self):
        self.required_fields = ["transaction_id", "amount", "date", "account"]
        self.errors = []
        self.valid_count=0
        self.invalid_count=0

    def parse_xml(self, file_path):
        tree = ET.parse(file_path)
        root = tree.getroot()
        transactions = []
        for transaction in root:
            trans_dict = {}
            for child in transaction:
                trans_dict[child.tag] = child.text
            transactions.append(trans_dict)
        return transactions

    def parse_json(self, file_path):
        with open(file_path, "r") as file:
            data = json.load(file)
            transactions = data["transactions"]
            return transactions

    def parse_csv(self, file_path):
        with open(file_path, "r") as file:
            data= csv.DictReader(file)
            transactions = [row for row in data]
            return transactions

    def validate_transaction(self, transaction):
        errors = []
        
        # 1. Check required fields
        for field in self.required_fields:
            if field not in transaction:
                errors.append(f"Missing required field: {field}")
        
        # 2. Validate amount
        if 'amount' in transaction:
            try:
                amount = float(transaction['amount'])
                if amount < 0:
                    errors.append("Amount cannot be negative")
                if amount > 1000000:
                    errors.append("Amount too large (over $1M)")
            except (ValueError, TypeError):
                errors.append("Amount must be a valid number")
        
        # 3. Validate date format
        if 'date' in transaction:
            try:
                datetime.strptime(transaction['date'], '%Y-%m-%d')
            except ValueError:
                errors.append("Invalid date format (should be YYYY-MM-DD)")
        
        # 4. Check for empty values
        for field in self.required_fields:
            if field in transaction and not transaction[field].strip():
                errors.append(f"Empty value for required field: {field}")
        
        return errors


