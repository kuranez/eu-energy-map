#!/usr/bin/env python3
"""
Simple test validation script to check if the testing setup works
without requiring pytest installation.
"""

import sys
import os
import pandas as pd
import geopandas as gpd
from pathlib import Path

def check_imports():
    """Check if required modules can be imported."""
    print("🔍 Checking imports...")
    
    try:
        # Add parent directory to path for imports
        parent_dir = Path(__file__).parent.parent
        sys.path.insert(0, str(parent_dir))
        
        from data.loader import load_data
        from data.filters import preprocess, filter_data
        from utils.flags import iso2_to_flag
        print("✅ All imports successful")
        return True
    except ImportError as e:
        print(f"❌ Import error: {e}")
        return False

def check_data_files():
    """Check if required data files exist."""
    print("\n🔍 Checking data files...")
    
    required_files = [
        './data/nrg_ind_ren_linear.csv',
        './geo/europe.geojson'
    ]
    
    missing_files = []
    for file_path in required_files:
        if not os.path.exists(file_path):
            missing_files.append(file_path)
    
    if missing_files:
        print(f"❌ Missing files: {missing_files}")
        return False
    else:
        print("✅ All required files found")
        return True

def test_basic_functionality():
    """Test basic functionality without pytest."""
    print("\n🧪 Testing basic functionality...")
    
    try:
        # Import functions for testing
        from data.loader import load_data
        from utils.flags import iso2_to_flag
        
        # Test flag conversion
        flag = iso2_to_flag("DE")
        assert flag == "🇩🇪", f"Expected 🇩🇪, got {flag}"
        print("✅ Flag conversion test passed")
        
        # Test data loading (basic)
        df = load_data()
        assert isinstance(df, pd.DataFrame), "Expected DataFrame"
        assert not df.empty, "DataFrame should not be empty"
        assert 'Flag' in df.columns, "Missing Flag column"
        print("✅ Data loading test passed")
        
        # Test raw data loading
        data, gdf = load_data(return_raw=True)
        assert isinstance(data, pd.DataFrame), "Expected DataFrame for data"
        assert isinstance(gdf, gpd.GeoDataFrame), "Expected GeoDataFrame for gdf"
        print("✅ Raw data loading test passed")
        
        return True
        
    except Exception as e:
        print(f"❌ Test failed: {e}")
        return False

def main():
    """Main validation function."""
    print("🧪 EU Energy Map - Test Validation")
    print("=" * 50)
    
    # Change to project root if needed
    if not os.path.exists('./data'):
        if os.path.exists('../data'):
            os.chdir('..')
        else:
            print("❌ Cannot find project root directory")
            return False
    
    success_count = 0
    total_tests = 3
    
    # Run validation checks
    if check_imports():
        success_count += 1
    
    if check_data_files():
        success_count += 1
    
    if test_basic_functionality():
        success_count += 1
    
    print(f"\n{'='*50}")
    print(f"🎯 Validation Summary: {success_count}/{total_tests} checks passed")
    print(f"{'='*50}")
    
    if success_count == total_tests:
        print("✅ All validation checks passed!")
        print("\n📋 Next steps:")
        print("1. Install pytest: pip install -r test/requirements.txt")
        print("2. Run full test suite: python -m pytest test/ -v")
        print("3. Generate coverage: python -m pytest test/ --cov=data --cov=utils")
        return True
    else:
        print("⚠️  Some validation checks failed.")
        print("Please check the errors above before running the full test suite.")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
