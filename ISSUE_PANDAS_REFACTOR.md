# Issue: Refactor Pandas Operations into Helper Functions

## 📋 **Issue Summary**

Currently, `data/filters.py` and `data/loader.py` contain redundant pandas operations that should be centralized into helper functions in `utils/helpers.py`. This refactoring will improve code maintainability, reduce duplication, and make the codebase more modular.

## 🎯 **Objectives**

- [ ] Extract common pandas operations into reusable helper functions
- [ ] Eliminate code duplication between `filters.py` and `loader.py`
- [ ] Improve testability by isolating data processing logic
- [ ] Maintain backward compatibility with existing API
- [ ] Add comprehensive error handling to new helper functions

## 🔍 **Current Issues**

### Identified Redundant Operations

1. **Energy Type Mapping** - Duplicated in both files
2. **Column Dropping** - Same columns dropped in both places
3. **Data Type Conversion** - Numeric conversion logic repeated
4. **Greece Country Code Remapping** - EL → GR mapping duplicated
5. **Flag Addition** - Same flag application logic
6. **Data Cleaning Pipeline** - Similar cleaning steps in both files

### Files Affected
- `data/filters.py` - Lines 11-25 (preprocessing operations)
- `data/loader.py` - Lines 39-56 (data processing operations)
- `utils/helpers.py` - Target file for new helper functions

## ✅ **Implementation Checklist**

### Phase 1: Create Helper Functions in `utils/helpers.py`

- [ ] **Create `map_energy_types()` function**
  ```python
  def map_energy_types(data: pd.DataFrame, custom_mapping: dict = None) -> pd.DataFrame
  ```
  - [ ] Default mapping for REN, REN_ELC, REN_HEAT_CL, REN_TRA
  - [ ] Support for custom energy type mappings
  - [ ] Error handling for missing 'Energy Type' column

- [ ] **Create `clean_columns()` function**
  ```python
  def clean_columns(data: pd.DataFrame, columns_to_drop: list = None) -> pd.DataFrame
  ```
  - [ ] Default list: ['LAST UPDATE', 'freq', 'unit', 'OBS_FLAG']
  - [ ] Support for custom column lists
  - [ ] Safe column dropping (ignore missing columns)

- [ ] **Create `convert_data_types()` function**
  ```python
  def convert_data_types(data: pd.DataFrame, numeric_columns: list = None) -> pd.DataFrame
  ```
  - [ ] Default numeric columns: ['Year', 'Renewable Percentage']
  - [ ] Round renewable percentages to 1 decimal place
  - [ ] Handle conversion errors gracefully

- [ ] **Create `remap_country_codes()` function**
  ```python
  def remap_country_codes(data: pd.DataFrame, code_mapping: dict = None) -> pd.DataFrame
  ```
  - [ ] Default mapping: {'EL': 'GR'} for Greece
  - [ ] Support for custom country code mappings
  - [ ] Apply to both 'CNTR_ID' and 'Code' columns

- [ ] **Create `add_country_flags()` function**
  ```python
  def add_country_flags(data: pd.DataFrame, code_column: str = 'Code') -> pd.DataFrame
  ```
  - [ ] Apply iso2_to_flag to specified column
  - [ ] Handle missing or invalid country codes
  - [ ] Create 'Flag' column

- [ ] **Create `process_energy_data()` function** (Complete Pipeline)
  ```python
  def process_energy_data(data: pd.DataFrame, **kwargs) -> pd.DataFrame
  ```
  - [ ] Combine all processing steps into one function
  - [ ] Accept parameters for customization
  - [ ] Maintain processing order: rename → map_types → clean → convert → remap → flags

### Phase 2: Update `data/filters.py`

- [ ] **Import new helper functions**
  ```python
  from utils.helpers import (
      merge_data, rename_columns, map_energy_types, 
      clean_columns, convert_data_types, remap_country_codes, 
      add_country_flags, process_energy_data
  )
  ```

- [ ] **Refactor `preprocess()` function**
  - [ ] Replace energy type mapping with `map_energy_types()`
  - [ ] Replace column dropping with `clean_columns()`
  - [ ] Replace data type conversion with `convert_data_types()`
  - [ ] Replace country code remapping with `remap_country_codes()`
  - [ ] Replace flag addition with `add_country_flags()`
  - [ ] Option: Use `process_energy_data()` for complete pipeline

- [ ] **Maintain function signature and behavior**
  - [ ] Ensure `preprocess()` returns same data structure
  - [ ] Preserve column order and data types
  - [ ] Keep same error handling behavior

### Phase 3: Update `data/loader.py`

- [ ] **Import new helper functions**
  ```python
  from utils.helpers import (
      load_csv_data, load_gdf, merge_data, rename_columns,
      process_energy_data  # Complete pipeline function
  )
  ```

- [ ] **Refactor `load_data()` function**
  - [ ] Replace manual processing steps with `process_energy_data()`
  - [ ] Keep existing error handling for file loading
  - [ ] Maintain return type and final column selection

- [ ] **Simplify processing pipeline**
  ```python
  # Before (lines 39-56)
  merged_data = rename_columns(merged_data)
  # ... 15+ lines of processing ...
  
  # After
  merged_data = process_energy_data(merged_data)
  ```

### Phase 4: Testing and Validation

- [ ] **Create tests for new helper functions**
  - [ ] Unit tests for each helper function
  - [ ] Integration tests for `process_energy_data()`
  - [ ] Edge case testing (missing columns, invalid data)

- [ ] **Update existing tests**
  - [ ] Ensure `test_filters.py` still passes
  - [ ] Ensure `test_loader.py` still passes
  - [ ] Add tests for error handling

- [ ] **Validation testing**
  - [ ] Compare output before/after refactoring
  - [ ] Ensure data integrity is maintained
  - [ ] Verify performance is not degraded

### Phase 5: Documentation and Cleanup

- [ ] **Update documentation**
  - [ ] Add docstrings for all new helper functions
  - [ ] Update `REFACTORING_GUIDE.md` with new functions
  - [ ] Update method list in `utils/helpers.py`

- [ ] **Code cleanup**
  - [ ] Remove commented old code
  - [ ] Ensure consistent code style
  - [ ] Add type hints to all new functions

- [ ] **Update CHANGELOG.md**
  - [ ] Document new helper functions
  - [ ] Note performance improvements
  - [ ] Mention reduced code duplication

## 🔧 **Technical Requirements**

### Function Specifications

Each helper function should:
- Accept pandas DataFrame as first parameter
- Return pandas DataFrame (or specified type)
- Include comprehensive error handling
- Support customization through optional parameters
- Maintain data immutability (create copies when needed)
- Include detailed docstrings with examples

### Error Handling Standards
```python
try:
    # Processing logic
    return processed_data
except Exception as e:
    logger.error(f"Error in function_name: {e}")
    return data  # Return original data on error
```

### Testing Standards
- Unit tests for each helper function
- Integration tests for combined operations
- Edge case testing (empty data, missing columns)
- Performance benchmarking

## 📊 **Expected Benefits**

- [ ] **Reduced Code Duplication**: ~40 lines of duplicated code eliminated
- [ ] **Improved Maintainability**: Single source of truth for data processing
- [ ] **Better Testability**: Individual functions can be tested in isolation
- [ ] **Enhanced Reusability**: Helper functions can be used by other modules
- [ ] **Consistent Error Handling**: Standardized error handling across operations

## 🚨 **Acceptance Criteria**

- [ ] All existing functionality remains unchanged
- [ ] No breaking changes to public APIs
- [ ] All tests pass
- [ ] Code coverage maintained or improved
- [ ] Documentation updated
- [ ] Performance not degraded

## 🔗 **Related Issues**

- Related to overall refactoring effort
- Follows patterns established in previous helper function additions
- Prepares codebase for future enhancements

## 💡 **Implementation Notes**

1. **Order Matters**: Maintain the current processing order to ensure consistent results
2. **Parameter Defaults**: Use sensible defaults that match current behavior
3. **Backward Compatibility**: Ensure existing code continues to work without changes
4. **Error Recovery**: Helper functions should fail gracefully and log errors
5. **Performance**: New functions should not introduce performance regressions

---

**Priority**: Medium  
**Estimated Effort**: 4-6 hours  
**Labels**: `refactoring`, `enhancement`, `good-first-issue`
