#!/usr/bin/env python3
"""
Test runner for EU Energy Map project.

This script runs all tests and generates coverage reports.
"""

import os
import sys
import subprocess
from pathlib import Path

def run_command(command, description):
    """Run a command and handle errors."""
    print(f"\n{'='*60}")
    print(f"🔄 {description}")
    print(f"{'='*60}")
    
    try:
        result = subprocess.run(command, shell=True, check=True, capture_output=True, text=True)
        print(result.stdout)
        if result.stderr:
            print("Warnings:", result.stderr)
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Error: {e}")
        print(f"stdout: {e.stdout}")
        print(f"stderr: {e.stderr}")
        return False

def check_requirements():
    """Check if required testing packages are installed."""
    required_packages = ['pytest', 'pytest-cov', 'coverage']
    missing_packages = []
    
    for package in required_packages:
        try:
            __import__(package.replace('-', '_'))
        except ImportError:
            missing_packages.append(package)
    
    if missing_packages:
        print(f"❌ Missing required packages: {missing_packages}")
        print("📦 Install with: pip install " + " ".join(missing_packages))
        return False
    
    return True

def main():
    """Main test runner function."""
    print("🧪 EU Energy Map - Test Runner")
    print("=" * 60)
    
    # Check if we're in the right directory
    if not Path('./data').exists() or not Path('./test').exists():
        print("❌ Please run this script from the project root directory")
        sys.exit(1)
    
    # Check requirements
    if not check_requirements():
        print("\n💡 You can still run tests manually with: python -m pytest test/")
        
    # Change to project root directory
    os.chdir('..')
    
    success_count = 0
    total_tests = 4
    
    # Run basic tests
    if run_command("python -m pytest test/ -v", "Running Basic Tests"):
        success_count += 1
    
    # Run tests with coverage
    if run_command("python -m pytest test/ --cov=data --cov=utils --cov-report=term-missing", 
                   "Running Tests with Coverage"):
        success_count += 1
    
    # Generate HTML coverage report
    if run_command("python -m pytest test/ --cov=data --cov=utils --cov-report=html", 
                   "Generating HTML Coverage Report"):
        success_count += 1
        print("📊 HTML coverage report generated in htmlcov/index.html")
    
    # Run specific test files
    if run_command("python -m pytest test/test_loader.py -v", "Testing Data Loader"):
        success_count += 1
    
    print(f"\n{'='*60}")
    print(f"🎯 Test Summary: {success_count}/{total_tests} test suites passed")
    print(f"{'='*60}")
    
    if success_count == total_tests:
        print("✅ All tests completed successfully!")
        return 0
    else:
        print("⚠️  Some tests failed. Please check the output above.")
        return 1

if __name__ == "__main__":
    sys.exit(main())