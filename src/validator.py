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

