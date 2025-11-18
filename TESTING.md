# Testing Guide for EU Energy Map

This document provides information about validating and testing the EU Energy Map project.

## 📋 Table of Contents

- [Overview](#overview)
- [Quick Validation](#quick-validation)
- [Validation Structure](#validation-structure)
- [Running Validation](#running-validation)
- [Advanced Testing](#advanced-testing)
- [Troubleshooting](#troubleshooting)

## 🎯 Overview

The EU Energy Map project uses a **lightweight validation approach** for quick setup verification. The validation script checks core functionality without requiring external testing frameworks.

### Validation Philosophy

- **Simplicity**: No external dependencies beyond project requirements
- **Fast Feedback**: Quick checks for imports, data files, and basic functionality
- **Self-Contained**: Single script validates entire setup
- **Zero Config**: Works out-of-the-box without additional setup

## 📁 Validation Structure

```
test/
├── validate_setup.py    # Standalone validation script
├── requirements.txt     # Optional: Advanced testing dependencies
└── README.md           # Testing documentation
```

### Validation Script Overview

**`validate_setup.py`** - Comprehensive setup validation:
- ✅ **Import Checks**: Verifies all modules can be imported
- ✅ **File Validation**: Confirms required data files exist
- ✅ **Functionality Tests**: Tests core data loading and processing
- ✅ **Flag Conversion**: Validates country flag emoji generation
- ✅ **Data Pipeline**: Ensures end-to-end processing works

## 🚀 Running Validation

### Quick Start

The simplest way to validate your setup:

```bash
# From project root
cd /home/kuranez/Projects/Python/Geo/EU-Energy-Map
python test/validate_setup.py
```

Or from the test directory:

```bash
cd test/
python validate_setup.py
```

### What Gets Validated

The validation script performs three main checks:

#### 1. Import Checks 🔍
Verifies all required modules can be imported:
- `data.loader.load_data`
- `data.filters.preprocess`, `filter_data`
- `utils.flags.iso2_to_flag`

#### 2. Data File Validation 📁
Confirms required data files exist:
- `./data/nrg_ind_ren_linear.csv` - Renewable energy data
- `./geo/europe.geojson` - European geographic boundaries

#### 3. Functionality Tests 🧪
Tests core application features:
- **Flag Conversion**: `iso2_to_flag("DE")` → `🇩🇪`
- **Data Loading**: Loads and validates merged DataFrame
- **Column Validation**: Ensures `Flag` column exists
- **Raw Data Loading**: Tests GeoDataFrame return functionality

### Expected Output

Successful validation shows:

```
🧪 EU Energy Map - Test Validation
==================================================
🔍 Checking imports...
✅ All imports successful

🔍 Checking data files...
✅ All required files found

🧪 Testing basic functionality...
✅ Flag conversion test passed
✅ Data loading test passed
✅ Raw data loading test passed

==================================================
🎯 Validation Summary: 3/3 checks passed
==================================================
✅ All validation checks passed!

📋 Next steps:
1. Install pytest: pip install -r test/requirements.txt
2. Run full test suite: python -m pytest test/ -v
3. Generate coverage: python -m pytest test/ --cov=data --cov=utils
```
## 🧪 Advanced Testing

### Optional: Install pytest

For advanced testing capabilities, you can install pytest:

```bash
pip install -r test/requirements.txt
```

This provides additional testing tools:
- `pytest` - Full-featured testing framework
- `pytest-cov` - Code coverage reporting
- `pytest-xdist` - Parallel test execution
- `pytest-html` - HTML test reports

### Running pytest Tests

If you create pytest test files, you can run them with:

```bash
# Run all tests with verbose output
python -m pytest test/ -v

# Run with coverage reporting
python -m pytest test/ --cov=data --cov=utils --cov-report=term-missing

# Generate HTML coverage report
python -m pytest test/ --cov=data --cov=utils --cov-report=html
# Open htmlcov/index.html in browser

# Parallel execution for faster tests
python -m pytest test/ -n auto
```

### Creating Custom Tests

You can extend the testing by creating pytest test files:

**Example: `test/test_custom.py`**
```python
import pytest
from data.loader import load_data
from utils.flags import iso2_to_flag

def test_greece_country_code():
    """Test that Greece is processed correctly with EL code."""
    df = load_data()
    greece_data = df[df['Code'] == 'EL']
    assert len(greece_data) > 0, "Greece data should exist with EL code"
    assert 'Flag' in greece_data.columns

@pytest.mark.parametrize("country,flag", [
    ("DE", "🇩🇪"), ("FR", "🇫🇷"), ("ES", "🇪🇸"),
    ("GR", "🇬🇷"),  # Greece flag from GR code
])
def test_flag_conversions(country, flag):
    """Test multiple country flag conversions."""
    assert iso2_to_flag(country) == flag

def test_data_completeness():
    """Test that loaded data has all required columns."""
    df = load_data()
    required_columns = ['Code', 'Flag', 'Country', 'Energy Type', 
                       'Renewable Percentage', 'Year', 'CNTR_ID', 'geometry']
    for col in required_columns:
        assert col in df.columns, f"Missing column: {col}"
```

## 🐛 Troubleshooting

### Common Issues

#### 1. Import Errors
```bash
# Error: ModuleNotFoundError: No module named 'data'
# Solution: Run validation from project root directory
cd /home/kuranez/Projects/Python/Geo/EU-Energy-Map
python test/validate_setup.py
```

The validation script automatically handles path issues by detecting and changing to the project root if needed.

#### 2. Missing Data Files
```bash
# Error: FileNotFoundError: Missing input data files
# Solution: Ensure data files exist in the correct locations
ls ./data/nrg_ind_ren_linear.csv
ls ./geo/europe.geojson
```

Required files:
- `data/nrg_ind_ren_linear.csv` - Renewable energy dataset
- `geo/europe.geojson` - European geographic boundaries

#### 3. Missing Dependencies
```bash
# Error: ModuleNotFoundError: No module named 'pandas'
# Solution: Install project dependencies
pip install -r requirements.txt
```

Required packages:
- `pandas` - Data manipulation
- `geopandas` - Geographic data handling
- `plotly` - Interactive visualizations
- `dash` - Web application framework

#### 4. Permission Errors
```bash
# Error: PermissionError: cannot access file
# Solution: Check file permissions
chmod 644 ./data/*.csv
chmod 644 ./geo/*.geojson
```

#### 5. Validation Fails on Specific Check

If a specific validation check fails:

**Import Check Failed** 🔍
- Verify all dependencies are installed: `pip install -r requirements.txt`
- Check Python version compatibility (3.8+)
- Ensure you're in the project directory

**Data File Check Failed** 📁
- Confirm data files are in correct locations
- Check file names match exactly (case-sensitive)
- Verify files aren't corrupted: try opening them manually

**Functionality Test Failed** 🧪
- Review error messages for specific failures
- Check data format hasn't changed
- Ensure helper functions are properly refactored

### Getting Help

If validation continues to fail:

1. **Check Error Messages**: Read the full error output carefully
2. **Verify Installation**: Ensure all dependencies are installed
3. **Check File Paths**: Confirm you're running from the correct directory
4. **Review Recent Changes**: If it worked before, check what changed
5. **Run Individual Checks**: Test components separately to isolate issues

### Manual Testing

You can manually test components:

```python
# Test imports
python -c "from data.loader import load_data; print('Import OK')"

# Test flag conversion
python -c "from utils.flags import iso2_to_flag; print(iso2_to_flag('DE'))"

# Test data loading
python -c "from data.loader import load_data; df = load_data(); print(f'Loaded {len(df)} rows')"
```

## 📚 Validation Script Details

### What the Script Does

The `validate_setup.py` script is a **self-contained validation tool** that:

1. **Auto-detects Project Root**: Finds the correct directory automatically
2. **Checks Imports**: Validates all modules can be loaded
3. **Verifies Data Files**: Confirms required CSV and GeoJSON files exist
4. **Tests Core Functions**: Runs basic functionality checks
5. **Provides Clear Feedback**: Shows ✅/❌ status for each check

### Validation Checks Breakdown

#### Check 1: Import Validation
```python
from data.loader import load_data
from data.filters import preprocess, filter_data
from utils.flags import iso2_to_flag
```

Ensures all core modules are accessible and error-free.

#### Check 2: File Validation
```python
required_files = [
    './data/nrg_ind_ren_linear.csv',
    './geo/europe.geojson'
]
```

Confirms data files are present and accessible.

#### Check 3: Functionality Tests
```python
# Flag conversion test
iso2_to_flag("DE") == "🇩🇪"

# Data loading test
df = load_data()
assert isinstance(df, pd.DataFrame)
assert 'Flag' in df.columns

# Raw data test
data, gdf = load_data(return_raw=True)
```

Validates that the application's core features work correctly.

### Exit Codes

The validation script uses standard exit codes:
- **0**: All checks passed ✅
- **1**: One or more checks failed ❌

This makes it suitable for CI/CD integration:
```bash
python test/validate_setup.py && echo "Validation passed" || echo "Validation failed"
```

## 🔗 Additional Resources

### Documentation
- [Pandas Documentation](https://pandas.pydata.org/docs/)
- [GeoPandas Documentation](https://geopandas.org/)
- [Plotly Dash Documentation](https://dash.plotly.com/)
- [pytest Documentation](https://docs.pytest.org/) (for advanced testing)

### Project Documentation
- `README.md` - Project overview and setup instructions
- `REFACTORING_GUIDE.md` - Architecture and development guide
- `CHANGELOG.md` - Change history and version information
- `test/README.md` - Testing pipeline documentation

## 🎯 Summary

### Current Testing Approach

The EU Energy Map uses a **simplified validation approach**:

✅ **Single validation script** (`validate_setup.py`)  
✅ **No external test framework required**  
✅ **Fast and lightweight** (runs in seconds)  
✅ **Self-contained** (includes all necessary checks)  
✅ **Clear feedback** (visual status indicators)

### When to Run Validation

Run the validation script:
- ✨ After initial project setup
- 🔄 After pulling new changes from repository
- 📦 After installing/updating dependencies
- 🛠️ After modifying core data processing code
- 🐛 When debugging issues
- 🚀 Before deploying or committing changes

### Benefits of This Approach

1. **Simplicity**: One script, zero configuration
2. **Speed**: Runs in seconds without heavy framework overhead
3. **Accessibility**: Easy for new contributors to understand
4. **Reliability**: Tests with actual project data
5. **Maintainability**: Single file to update as project evolves

---

## 🤝 Contributing

When contributing to the project, please:

1. ✅ **Run validation before committing**: `python test/validate_setup.py`
2. 📝 **Update validation script** if adding new core modules
3. 🧪 **Add checks** for new critical functionality
4. 📖 **Document changes** in validation behavior
5. 🔍 **Test edge cases** manually for complex changes

### Future Testing Enhancements

If the project grows, consider adding:
- Full pytest test suite with unit tests
- Integration tests for UI components
- Performance benchmarking tests
- Data quality validation tests
- Automated CI/CD pipeline testing

For now, the lightweight validation approach provides the right balance of simplicity and coverage for the project's needs.

---

**Last Updated**: November 2025  
**Validation Script Version**: 1.0
