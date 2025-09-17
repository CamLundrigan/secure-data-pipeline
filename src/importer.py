import sqlite3
import os
from datetime import datetime

class DataImporter:
    def __init__(self, db_path="financial_data.db"):
        self.db_path = db_path
        self.conn = sqlite3.connect(db_path)
        self.cursor = self.conn.cursor()
        

    def create_table(self):
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS transactions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                transaction_id TEXT UNIQUE NOT NULL,
                amount REAL NOT NULL,
                date TEXT NOT NULL,
                account TEXT NOT NULL,
                description TEXT,
                merchant TEXT,
                imported_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        self.conn.commit()
        
    def insert_transaction(self, transaction):
        self.cursor.execute('''
            INSERT INTO transactions (transaction_id, amount, date, account, description, merchant)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (
            transaction["transaction_id"],
            float(transaction["amount"]),
            transaction["date"],
            transaction["account"],
            transaction.get("description", ""),
            transaction.get("merchant", "")
        ))
        self.conn.commit()
        
    def import_transactions(self, transactions):
        for transaction in transactions:
            self.insert_transaction(transaction)
            
    def close(self):
        self.conn.close()
        
        