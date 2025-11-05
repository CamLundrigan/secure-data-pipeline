import os
from src.sftp_transfer import SFTPClient
from src.validator import DataValidator
from src.importer import DataImporter

class FinancialDataPipeline:
    def __init__(self, sftp_host="test.rebex.net", sftp_user="demo", sftp_pass="password"):
        self.sftp = SFTPClient(sftp_host, sftp_user, sftp_pass)
        self.validator = DataValidator()
        self.importer = DataImporter("financial_data.db")
        
    def process_sftp_files(self, remote_directory="/", local_directory="./downloaded_files"):
        """Download files from SFTP, validate, and import to database"""
        print("=== Starting Financial Data Pipeline ===")
        
        # Create local directory if it doesn't exist
        if not os.path.exists(local_directory):
            os.makedirs(local_directory)
        
        try:
            # Step 1: Connect to SFTP
            print("1. Connecting to SFTP server...")
            self.sftp.connect()
            
            # Step 2: List available files
            print("2. Listing available files...")
            files = self.sftp.list_files(remote_directory)
            
            # Step 3: Download and process each file
            total_processed = 0
            total_valid = 0
            
            for file in files:
                if file.endswith(('.csv', '.json', '.xml')):
                    print(f"3. Processing {file}...")
                    
                    # Download file
                    remote_path = f"{remote_directory}/{file}" if remote_directory != "/" else f"/{file}"
                    local_path = os.path.join(local_directory, file)
                    
                    if self.sftp.download_file(remote_path, local_path):
                        # Process the downloaded file
                        valid_count = self.process_file(local_path)
                        total_processed += 1
                        total_valid += valid_count
                        print(f"   Processed {file}: {valid_count} valid transactions")
            
            print(f"\n=== Pipeline Complete ===")
            print(f"Files processed: {total_processed}")
            print(f"Valid transactions imported: {total_valid}")
            
        finally:
            # Always disconnect
            self.sftp.disconnect()
    
    def process_file(self, file_path):
        """Process a single file: validate and import valid transactions"""
        try:
            # Determine file type and parse
            if file_path.endswith('.json'):
                transactions = self.validator.parse_json(file_path)
            elif file_path.endswith('.csv'):
                transactions = self.validator.parse_csv(file_path)
            elif file_path.endswith('.xml'):
                transactions = self.validator.parse_xml(file_path)
            else:
                print(f"   Skipping unsupported file: {file_path}")
                return 0
            
            # Validate each transaction
            valid_transactions = []
            for transaction in transactions:
                errors = self.validator.validate_transaction(transaction)
                if not errors:  # No errors = valid
                    valid_transactions.append(transaction)
            
            # Import valid transactions to database
            if valid_transactions:
                self.importer.create_table()  # Ensure table exists
                self.importer.import_transactions(valid_transactions)
            
            return len(valid_transactions)
            
        except Exception as e:
            print(f"   Error processing {file_path}: {e}")
            return 0
    
    def process_local_files(self, file_directory="./sample_data"):
        """Process local files without SFTP (for testing)"""
        print("=== Processing Local Files ===")
        
        if not os.path.exists(file_directory):
            print(f"Directory {file_directory} not found")
            return
        
        files = [f for f in os.listdir(file_directory) if f.endswith(('.csv', '.json', '.xml'))]
        
        total_valid = 0
        for file in files:
            file_path = os.path.join(file_directory, file)
            print(f"Processing {file}...")
            valid_count = self.process_file(file_path)
            total_valid += valid_count
            print(f"  {valid_count} valid transactions imported")
        
        print(f"\nTotal valid transactions imported: {total_valid}")
    
    def get_database_summary(self):
        """Get summary of data in database"""
        try:
            self.importer.cursor.execute("SELECT COUNT(*) FROM transactions")
            count = self.importer.cursor.fetchone()[0]
            
            self.importer.cursor.execute("SELECT COUNT(*) FROM transactions WHERE amount > 10000")
            suspicious = self.importer.cursor.fetchone()[0]
            
            print(f"\n=== Database Summary ===")
            print(f"Total transactions: {count}")
            print(f"Suspicious transactions (>$10,000): {suspicious}")
            
        except Exception as e:
            print(f"Error getting database summary: {e}")
