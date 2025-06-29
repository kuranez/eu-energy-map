# utils/mapping.py

import pandas as pd

from config import (
    ENERGY_TYPE_MAPPING,
    COUNTRY_CODE_MAPPING,
    EU_COUNTRIES,
    COLUMN_MAPPING,
    COLUMNS_TO_DROP
)

"""
Data mapping utilities for EU Energy Map project.
Contains various functions for data standardization.
"""

def get_energy_type_mapping(custom_mapping: dict | None = None) -> dict:
    """
    Get energy type mapping dictionary.
    
    Args:
        custom_mapping (dict, optional): Custom mapping to override defaults
        
    Returns:
        dict: Energy type mapping dictionary
    """
    if custom_mapping:
        return {**ENERGY_TYPE_MAPPING, **custom_mapping}
    return ENERGY_TYPE_MAPPING.copy()

def get_country_code_mapping(custom_mapping: dict | None = None) -> dict:
    """
    Get country code mapping dictionary.
    
    Args:
        custom_mapping (dict, optional): Custom mapping to override defaults
        
    Returns:
        dict: Country code mapping dictionary
    """
    if custom_mapping:
        return {**COUNTRY_CODE_MAPPING, **custom_mapping}
    return COUNTRY_CODE_MAPPING.copy()

def get_eu_countries(additional_countries: set | None = None) -> set:
    """
    Get set of EU country codes.
    
    Args:
        additional_countries (set, optional): Additional countries to include
        
    Returns:
        set: Set of EU country codes
    """
    if additional_countries:
        return EU_COUNTRIES.union(additional_countries)
    return EU_COUNTRIES.copy()

def get_column_mapping(custom_mapping: dict | None = None) -> dict:
    """
    Get column mapping dictionary.
    
    Args:
        custom_mapping (dict, optional): Custom mapping to override defaults
        
    Returns:
        dict: Column mapping dictionary
    """
    if custom_mapping:
        return {**COLUMN_MAPPING, **custom_mapping}
    return COLUMN_MAPPING.copy()

def get_columns_to_drop(additional_columns: list | None = None) -> list:
    """
    Get list of columns to drop during cleaning.
    
    Args:
        additional_columns (list, optional): Additional columns to drop
        
    Returns:
        list: List of column names to drop
    """
    columns = COLUMNS_TO_DROP.copy()
    if additional_columns:
        columns.extend(additional_columns)
    return columns

def apply_column_mapping(data: pd.DataFrame, custom_mapping: dict | None = None) -> pd.DataFrame:
    """
    Apply column mappings to the DataFrame.
        
    Args:
        data (pd.DataFrame): DataFrame to apply mappings to
        custom_mapping (dict, optional): Custom mapping to override defaults

    Returns:
        pd.DataFrame: DataFrame with column mappings applied
    """
    try:
        mapping = get_column_mapping(custom_mapping)
        data = data.rename(columns=mapping, errors='ignore')
        return data
    except Exception as e:
        print(f"Error applying column mapping: {e}")
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