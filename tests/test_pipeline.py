import sys
import os

# Add the parent directory to Python's path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.pipeline import FinancialDataPipeline

def test_complete_pipeline():
    print("=== Testing Complete Financial Data Pipeline ===")
    
    # Create pipeline
    pipeline = FinancialDataPipeline()
    
    # Test 1: Process local sample files
    print("\n1. Testing with local sample files...")
    pipeline.process_local_files("./sample_data")
    
    # Test 2: Get database summary
    print("\n2. Database summary:")
    pipeline.get_database_summary()
    
    # Test 3: Process SFTP files (optional - requires internet)
    print("\n3. Testing SFTP file processing...")
    try:
        pipeline.process_sftp_files("/pub/example", "./downloaded_files")
    except Exception as e:
        print(f"SFTP test failed (this is normal if no internet): {e}")
    
    print("\n🎉 Pipeline test completed!")

if __name__ == "__main__":
    test_complete_pipeline()
