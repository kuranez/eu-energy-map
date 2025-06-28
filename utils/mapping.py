# utils/mapping.py

"""
Data mapping utilities for EU Energy Map project.
Contains various mapping dictionaries and functions for data standardization.
"""

# Energy type mappings from Eurostat codes to human-readable names
ENERGY_TYPE_MAPPING = {
    'REN': 'Renewable Energy Total',
    'REN_ELC': 'Renewable Electricity',
    'REN_HEAT_CL': 'Renewable Heating and Cooling',
    'REN_TRA': 'Renewable Energy in Transport'
}

# Country code mappings for data standardization
COUNTRY_CODE_MAPPING = {
    'EL': 'GR'  # Greece: EL (Eurostat) -> GR (ISO standard)
}

# EU member countries (as of 2025)
EU_COUNTRIES = {
    "AT", "BE", "BG", "HR", "CY", "CZ", "DK", "EE", "FI", "FR", 
    "DE", "GR", "HU", "IE", "IT", "LV", "LT", "LU", "MT", "NL", 
    "PL", "PT", "RO", "SK", "SI", "ES", "SE"
}

# Column mappings for data standardization
COLUMN_MAPPING = {
    'nrg_bal': 'Energy Type',
    'TIME_PERIOD': 'Year',
    'OBS_VALUE': 'Renewable Percentage',
    'geo': 'Code',
    'NAME_ENGL': 'Country'
}

# Columns to drop during data cleaning
COLUMNS_TO_DROP = ['LAST UPDATE', 'freq', 'unit', 'OBS_FLAG']

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
