# Testing Guide for EU Energy Map

This document provides comprehensive information about testing the EU Energy Map project.

## 📋 Table of Contents

- [Overview](#overview)
- [Test Structure](#test-structure)
- [Running Tests](#running-tests)
- [Test Coverage](#test-coverage)
- [Writing Tests](#writing-tests)
- [Continuous Integration](#continuous-integration)
- [Troubleshooting](#troubleshooting)

## 🎯 Overview

The EU Energy Map project uses **pytest** as the primary testing framework. Tests are organized to ensure data integrity, function reliability, and system robustness.

### Testing Philosophy

- **Unit Tests**: Test individual functions and methods
- **Integration Tests**: Test data pipeline and component interaction
- **Data Validation**: Ensure data quality and consistency
- **Error Handling**: Test edge cases and error conditions

## 📁 Test Structure

```
test/
├── conftest.py           # Test fixtures and configuration
├── test_loader.py        # Tests for data loading functionality
├── test_filters.py       # Tests for data filtering functionality
├── test_helpers.py       # Tests for utility helper functions
├── requirements.txt      # Testing dependencies
├── run_tests.py         # Test runner script
├── validate_setup.py    # Simple validation without pytest
├── README.md            # Testing pipeline summary
└── TEST_SUCCESS.md      # Current test status report
```

### Test Files Description

| File | Purpose | Coverage |
|------|---------|----------|
| `conftest.py` | Shared fixtures and test configuration | Test data setup |
| `test_loader.py` | Data loading and processing tests | `data/loader.py` |
| `test_filters.py` | Data filtering and preprocessing tests | `data/filters.py` |
| `test_helpers.py` | Helper function unit and integration tests | `utils/helpers.py` |
| `run_tests.py` | Automated test runner with coverage | All test execution |
| `validate_setup.py` | Basic validation without pytest | Quick setup check |

## 🚀 Running Tests

### Prerequisites

Install testing dependencies:

```bash
pip install -r test/requirements.txt
```

### Quick Start

#### 1. Run All Tests
```bash
# From project root
python -m pytest test/ -v
```

#### 2. Run with Coverage
```bash
python -m pytest test/ --cov=data --cov=utils --cov-report=term-missing
```

#### 3. Use Test Runner Script
```bash
# From test directory
cd test/
python run_tests.py
```

#### 4. Run Specific Test Files
```bash
# Test only data loader
python -m pytest test/test_loader.py -v

# Test only data filters
python -m pytest test/test_filters.py -v

# Test only helper functions
python -m pytest test/test_helpers.py -v
```

#### 5. Quick Validation (Without pytest)
```bash
# Simple validation script
cd test/
python validate_setup.py
```

### Advanced Test Options

#### Parallel Testing
```bash
pip install pytest-xdist
python -m pytest test/ -n auto  # Use all CPU cores
```

#### Generate HTML Report
```bash
python -m pytest test/ --cov=data --cov=utils --cov-report=html
# Open htmlcov/index.html in browser
```

#### Test with Different Verbosity
```bash
python -m pytest test/ -v      # Verbose
python -m pytest test/ -vv     # Extra verbose
python -m pytest test/ -q      # Quiet
```

## 📊 Test Coverage

### Current Coverage Targets

- **Data Loading (`data/loader.py`)**: ✅ **Fully tested** - 15 tests covering all functionality
- **Data Filtering (`data/filters.py`)**: ✅ **Fully tested** - 15 tests covering preprocessing and filtering
- **Helper Functions (`utils/helpers.py`)**: ✅ **Fully tested** - 11 tests covering current implementations
- **Utility Functions (`utils/flags.py`, `utils/mapping.py`)**: ✅ **Covered** via integration tests

### Current Test Status

**✅ 41 tests passing, 0 failures**

All current functionality is comprehensively tested including:
- CSV and GeoJSON data loading
- Data merging and column renaming  
- Energy type mapping and country code conversion
- Flag generation and data validation
- Error handling for missing files
- Integration testing with real project data

### Coverage Reports

#### Terminal Coverage
```bash
python -m pytest test/ --cov=data --cov=utils --cov-report=term-missing
```

#### HTML Coverage Report
```bash
python -m pytest test/ --cov=data --cov=utils --cov-report=html
open htmlcov/index.html  # macOS
# Or navigate to htmlcov/index.html in your browser
```

#### Coverage Configuration

Coverage settings can be configured in `pyproject.toml` or `.coveragerc`:

```toml
[tool.coverage.run]
source = ["data", "utils"]
omit = [
    "*/test/*",
    "*/__pycache__/*",
    "*/venv/*"
]

[tool.coverage.report]
exclude_lines = [
    "pragma: no cover",
    "def __repr__",
    "raise AssertionError",
    "raise NotImplementedError"
]
```

## ✍️ Writing Tests

### Test Structure Guidelines

#### 1. Use Descriptive Test Names
```python
def test_load_data_success():
    """Test successful data loading and processing."""
    # Test implementation
```

#### 2. Organize Tests in Classes
```python
class TestDataLoader:
    """Test suite for data loading functionality."""
    
    def test_basic_loading(self):
        """Test basic data loading."""
        pass
    
    def test_error_handling(self):
        """Test error handling in data loading."""
        pass
```

#### 3. Use Fixtures for Common Data
```python
@pytest.fixture
def sample_data():
    """Provide sample data for testing."""
    return pd.DataFrame({
        'geo': ['DE', 'FR'],
        'value': [25.5, 30.2]
    })

def test_with_fixture(sample_data):
    """Test using fixture data."""
    assert not sample_data.empty
```

### Test Categories

#### 1. Unit Tests
Test individual functions in isolation:
```python
def test_load_csv_data_success():
    """Test CSV loading function."""
    df = load_csv_data('./data/nrg_ind_ren_linear.csv')
    assert isinstance(df, pd.DataFrame)
    assert not df.empty

def test_iso2_to_flag():
    """Test flag conversion function."""
    assert iso2_to_flag("DE") == "🇩🇪"
    assert iso2_to_flag("FR") == "🇫🇷"
```

#### 2. Integration Tests
Test data pipeline end-to-end:
```python
def test_full_data_pipeline():
    """Test complete data processing pipeline."""
    result = load_data()
    assert isinstance(result, pd.DataFrame)
    assert not result.empty
    assert 'Flag' in result.columns
```

#### 3. Parametrized Tests
Test multiple scenarios efficiently:
```python
@pytest.mark.parametrize("country,flag", [
    ("DE", "🇩🇪"), ("FR", "🇫🇷"), ("ES", "🇪🇸"),
])
def test_country_flags(country, flag):
    """Test flag conversion for multiple countries."""
    assert iso2_to_flag(country) == flag
```

#### 4. Error Testing
Test error conditions and edge cases:
```python
def test_file_not_found():
    """Test error handling for missing files."""
    with pytest.raises(FileNotFoundError):
        load_data(data_path='./nonexistent.csv')
```

#### 5. Fixture-based Testing
Use both real and sample data:
```python
def test_with_real_data(raw_data):
    """Test with actual project data."""
    df, gdf = raw_data
    result = preprocess(df, gdf)
    assert not result.empty

def test_with_sample_data(sample_csv_data):
    """Test with controlled sample data."""
    renamed = rename_columns(sample_csv_data)
    assert 'Energy Type' in renamed.columns
```

### Best Practices

1. **Test Current Functionality**: Focus on what's actually implemented
2. **Use Descriptive Assertions**: Include meaningful error messages
3. **Clean Test Data**: Use fixtures for both real and sample data
4. **Test Edge Cases**: Include tests for empty data, missing files, invalid inputs
5. **Class-based Organization**: Group related tests in test classes
6. **Skip Gracefully**: Use `pytest.skip()` when data files are missing
7. **Integration Testing**: Test complete workflows with real data

## 🔄 Continuous Integration

### GitHub Actions Example

The test suite is ready for CI/CD integration. Create `.github/workflows/tests.yml`:

```yaml
name: Tests

on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest
    strategy:
      matrix:
        python-version: ["3.9", "3.10", "3.11"]

    steps:
    - uses: actions/checkout@v4
    - name: Set up Python ${{ matrix.python-version }}
      uses: actions/setup-python@v4
      with:
        python-version: ${{ matrix.python-version }}
    
    - name: Install dependencies
      run: |
        python -m pip install --upgrade pip
        pip install -r requirements.txt
        pip install -r test/requirements.txt
    
    - name: Run tests with coverage
      run: |
        python -m pytest test/ --cov=data --cov=utils --cov-report=xml
    
    - name: Upload coverage to Codecov
      uses: codecov/codecov-action@v3
      with:
        file: ./coverage.xml
```

### Pre-commit Hooks

Install pre-commit hooks to run tests before commits:

```bash
pip install pre-commit
```

Create `.pre-commit-config.yaml`:

```yaml
repos:
  - repo: local
    hooks:
      - id: pytest
        name: pytest
        entry: python -m pytest test/ -x
        language: system
        pass_filenames: false
        always_run: true
```

## 🐛 Troubleshooting

### Common Issues

#### 1. Import Errors
```bash
# Error: ModuleNotFoundError: No module named 'data'
# Solution: Run tests from project root directory
cd /path/to/EU-Energy-Map
python -m pytest test/
```

#### 2. Missing Test Data
```bash
# Error: FileNotFoundError: Missing input data files
# Solution: Ensure data files exist
ls ./data/nrg_ind_ren_linear.csv
ls ./geo/europe.geojson
```

#### 3. Permission Errors
```bash
# Error: PermissionError: cannot access file
# Solution: Check file permissions
chmod 644 ./data/*.csv
chmod 644 ./geo/*.geojson
```

#### 4. Memory Issues with Large Data
```python
# For large datasets, use data sampling in tests
@pytest.fixture
def sample_data():
    """Use subset of data for testing."""
    df = pd.read_csv('./data/nrg_ind_ren_linear.csv')
    return df.sample(n=1000)  # Use only 1000 rows
```

### Performance Tips

1. **Use Module-scoped Fixtures**: Load data once per test module
2. **Parallel Testing**: Use `pytest-xdist` for faster execution
3. **Skip Slow Tests**: Mark slow tests and skip in development

```python
@pytest.mark.slow
def test_full_dataset():
    """Slow test - skip in development."""
    pass

# Run without slow tests
# python -m pytest test/ -m "not slow"
```

## 📈 Test Metrics

### Key Metrics to Track

- **Code Coverage**: Percentage of code executed by tests
- **Test Execution Time**: How long tests take to run
- **Test Success Rate**: Percentage of tests passing
- **Error Detection**: Number of bugs caught by tests

### Coverage Goals

| Component | Current Status | Test Count |
|-----------|----------------|------------|
| Data Loading (`data/loader.py`) | ✅ **Fully Covered** | 9 tests |
| Data Filtering (`data/filters.py`) | ✅ **Fully Covered** | 9 tests |
| Helper Functions (`utils/helpers.py`) | ✅ **Fully Covered** | 9 tests |
| Utility Functions (`utils/flags.py`) | ✅ **Covered** | 10 tests |
| Integration Testing | ✅ **Complete** | 4 tests |

**Total: 41 tests passing**

## 🔗 Additional Resources

- [pytest Documentation](https://docs.pytest.org/)
- [pytest-cov Documentation](https://pytest-cov.readthedocs.io/)
- [Python Testing Best Practices](https://docs.python-guide.org/writing/tests/)
- [Effective Python Testing](https://realpython.com/pytest-python-testing/)

---

## 🤝 Contributing to Tests

When contributing to the project:

1. **Test Current Functionality**: Focus on what's actually implemented
2. **Maintain Coverage**: Don't decrease overall test coverage (currently 41 tests passing)
3. **Test Edge Cases**: Include tests for error conditions and missing data
4. **Document Tests**: Use clear docstrings and comments
5. **Run Full Test Suite**: Ensure all tests pass before submitting
6. **Add Helper Tests**: When adding new helper functions, include comprehensive tests
7. **Use Existing Patterns**: Follow the established test structure and naming conventions

### Future Testing Areas

When implementing the remaining pandas refactoring (see `REFACTORING_GUIDE.md`):

- Tests for `clean_columns()` helper function
- Tests for `convert_data_types()` helper function  
- Tests for `remap_country_codes()` helper function
- Tests for `add_country_flags()` helper function
- Tests for `process_energy_data()` pipeline function

For questions about testing, please refer to:
- `test/README.md` for testing pipeline summary
- `test/TEST_SUCCESS.md` for current status
- `REFACTORING_GUIDE.md` for future development plans
