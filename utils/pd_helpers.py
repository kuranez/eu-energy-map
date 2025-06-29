# utils/pd_helpers.py

"""
Pandas helper functions for EU Energy Map project.
Contains data processing, cleaning, and transformation utilities.
"""

import pandas as pd
from utils.import_helpers import (
    get_column_mapping, get_columns_to_drop, get_country_code_mapping,
    get_energy_type_mapping, get_eu_countries
)

def merge_data(europe: pd.DataFrame, data: pd.DataFrame, 
               left_key: str = 'CNTR_ID', right_key: str = 'geo') -> pd.DataFrame:
    """
    Merge Europe GeoDataFrame with CSV data on specified keys.
    
    Args:
        europe (pd.DataFrame): Europe geographic data
        data (pd.DataFrame): CSV data to merge
        left_key (str): Column name in europe data to merge on
        right_key (str): Column name in CSV data to merge on
        
    Returns:
        pd.DataFrame: Merged data
    """
    try:
        merged = europe.merge(data, left_on=left_key, right_on=right_key)
        return merged
    except Exception as e:
        print(f"Error merging data: {e}")
        return pd.DataFrame()  # Return empty DataFrame on error

def rename_columns(data: pd.DataFrame, custom_mapping: dict | None = None) -> pd.DataFrame:
    """
    Rename columns to standardized format for energy data.
    
    Args:
        data (pd.DataFrame): DataFrame to rename columns for
        custom_mapping (dict, optional): Custom column mapping to override defaults
        
    Returns:
        pd.DataFrame: DataFrame with renamed columns
    """
    # Use centralized column mapping
    column_mapping = get_column_mapping(custom_mapping)
    
    try:
        # Create a copy to avoid modifying original data
        renamed_data = data.copy()
        renamed_data.rename(columns=column_mapping, inplace=True)
        return renamed_data
    except Exception as e:
        print(f"Error renaming columns: {e}")
        return data  # Return original data on error

def convert_data_types(data: pd.DataFrame, columns: list[str]) -> pd.DataFrame:
    """
    Convert specified columns to numeric and round values.
    
    Args:
        data (pd.DataFrame): DataFrame to convert columns for
        columns (list[str]): List of column names to convert
        
    Returns:
        pd.DataFrame: DataFrame with specified columns converted to numeric and rounded
    """
    try:
        for col in columns:
            if col in data.columns:
                data[col] = pd.to_numeric(data[col], errors='coerce').round(1)
        return data
    except Exception as e:
        print(f"Error converting columns: {e}")
        return data  # Return original data on error

def remap_country_codes(data: pd.DataFrame, code_mapping: dict | None = None, 
                        columns_to_remap: list[str] | None = None) -> pd.DataFrame:
    """
    Convert country codes in the DataFrame to standardized format.
    
    IMPORTANT: For Greece mapping issue fix - only remap 'Code' column for flag display,
    keep CNTR_ID as 'EL' to maintain consistency with geographic data.
    
    Args:
        data (pd.DataFrame): DataFrame with country codes to convert
        code_mapping (dict, optional): Custom mapping to override defaults
        columns_to_remap (list[str], optional): Specific columns to remap. 
                                               If None, remaps only 'Code' column (for flag display)
        
    Returns:
        pd.DataFrame: DataFrame with country codes converted
    """
    try:
        # Use centralized country code mapping if no custom mapping provided
        mapping = get_country_code_mapping(code_mapping) if code_mapping else get_country_code_mapping()
        
        # Default to only remapping 'Code' column (for flag display)
        # Leave CNTR_ID as-is to maintain consistency with geographic data
        columns = columns_to_remap if columns_to_remap else ['Code']
        
        for col in columns:
            if col in data.columns:
                data[col] = data[col].replace(mapping)
                
        return data
    except Exception as e:
        print(f"Error converting country codes: {e}")
        return data  # Return original data on error

def clean_columns(data: pd.DataFrame, columns_to_drop: list[str] | None = None) -> pd.DataFrame:
    """
    Clean the DataFrame by dropping unnecessary columns.
    
    Args:
        data (pd.DataFrame): DataFrame to clean
        columns_to_drop (list[str], optional): List of column names to drop
        
    Returns:
        pd.DataFrame: DataFrame with specified columns dropped
    """
    # Use centralized columns to drop
    columns = get_columns_to_drop(columns_to_drop) if columns_to_drop else get_columns_to_drop()
    
    try:
        return data.drop(columns=columns, errors='ignore')
    except Exception as e:
        print(f"Error cleaning columns: {e}")
        return data  # Return original data on error

def add_country_flags(data: pd.DataFrame, code_column: str = 'Code') -> pd.DataFrame:
    """
    Add country flags to the DataFrame using ISO2 country codes.
    
    Args:
        data (pd.DataFrame): DataFrame to add flags to
        code_column (str): Column name containing ISO2 country codes
        
    Returns:
        pd.DataFrame: DataFrame with Flag column added
    """
    try:
        from utils.flags import iso2_to_flag
        if code_column in data.columns:
            data['Flag'] = data[code_column].apply(iso2_to_flag)
        return data
    except Exception as e:
        print(f"Error adding country flags: {e}")
        return data  # Return original data on error

def apply_energy_type_mapping(data: pd.DataFrame, custom_mapping: dict | None = None, 
                             column_name: str = 'Energy Type') -> pd.DataFrame:
    """
    Apply energy type mappings to the DataFrame.
    
    Args:
        data (pd.DataFrame): DataFrame to apply mappings to
        custom_mapping (dict, optional): Custom mapping to override defaults
        column_name (str): Column name containing energy type codes
        
    Returns:
        pd.DataFrame: DataFrame with energy type mappings applied
    """
    try:
        if column_name in data.columns:
            mapping = get_energy_type_mapping(custom_mapping)
            data[column_name] = data[column_name].replace(mapping)
        return data
    except Exception as e:
        print(f"Error applying energy type mapping: {e}")
        return data  # Return original data on error

def filter_eu_countries(data: pd.DataFrame, code_column: str = 'Code', 
                        additional_countries: set | None = None) -> pd.DataFrame:
    """
    Filter DataFrame to include only EU countries.
    
    Args:
        data (pd.DataFrame): DataFrame to filter
        code_column (str): Column name containing country codes
        additional_countries (set, optional): Additional countries to include
        
    Returns:
        pd.DataFrame: Filtered DataFrame with EU countries only
    """
    try:
        if code_column in data.columns:
            eu_countries = get_eu_countries(additional_countries)
            return data[data[code_column].isin(eu_countries)]
        return data
    except Exception as e:
        print(f"Error filtering EU countries: {e}")
        return data  # Return original data on error
