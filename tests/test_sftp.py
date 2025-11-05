import sys
import os

# Add the parent directory to Python's path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.sftp_transfer import SFTPClient

def test_sftp():
    print("=== Testing SFTP Client ===")
    
    # Create SFTP client
    sftp = SFTPClient("test.rebex.net", "demo", "password")
    
    try:
        # Connect
        sftp.connect()
        
        # List files
        files = sftp.list_files("/")
        print(f"Found {len(files)} files")
        
        # Download a test file
        sftp.download_file("/pub/example/readme.txt", "downloaded_readme.txt")
        
    finally:
        # Always disconnect
        sftp.disconnect()
    
    print(" SFTP test completed!")

if __name__ == "__main__":
    test_sftp()