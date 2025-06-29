# utils/helpers.py
import os
import glob
import json
import pandas as pd
import geopandas as gpd
# import panel as pn  # Assuming you are using Panel for caching

# =============================================================================
# MAPPING CONSTANTS AND FUNCTIONS (from mapping.py)
# =============================================================================

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

# =============================================================================
# HELPER FUNCTIONS
# =============================================================================

# Method List:
# 1. load_csv_data: Simple CSV loading function
# 2. load_and_combine_csv_data: Enhanced CSV loading function that combines multiple files  
# 3. load_geojson: Function to load GeoJSON data
# 4. load_gdf: Function to load GeoJSON data as a GeoDataFrame
# 5. merge_data: Function to merge Europe GeoDataFrame with CSV data
# 6. rename_columns: Function to rename columns to standardized format
# 7. convert_data_types: Function to convert columns to numeric and round values
# 8. remap_country_codes: Function to convert country codes to standardized format
# 9. clean_columns: Function to clean columns by removing unnecessary ones
# 10. add_country_flags: Function to add country flags using ISO2 codes
# 11. apply_energy_type_mapping: Function to apply energy type mappings
# 12. filter_eu_countries: Function to filter DataFrame to EU countries only

# Simple CSV loading function
# @pn.cache
def load_csv_data(file_path):
    """
    Load CSV data from a given file path and handle potential mixed types.
    """
    try:
        # Attempt to load the CSV with low_memory=False to avoid dtype inference warnings
        return pd.read_csv(file_path, low_memory=False)
    except Exception as e:
        print(f"Error loading CSV: {e}")
        return None

# Enhanced CSV loading function
# @pn.cache
def load_and_combine_csv_data(file_path):
    """
    Loads and combines multiple CSV files from the specified folder.
    Handles potential dtype issues and suppresses warnings.
    Returns the combined dataset as a DataFrame.
    """
    # # Get all CSV files in the folder
    # csv_files = glob.glob(os.path.join(file_path, "*.csv"))
    
    # Get all CSV files matching the pattern `estat_nrg_cb_*`
    csv_files = glob.glob(os.path.join(file_path, "estat_nrg_cb_*.csv"))
    
    # Load and combine all matching CSV files into a single DataFrame
    data_frames = []
    for file in csv_files:
        try:
            # Load each file with low_memory=False to suppress DtypeWarning
            df = pd.read_csv(file, low_memory=False)
            data_frames.append(df)
        except Exception as e:
            print(f"Error loading file {file}: {e}")
    
    # Combine all loaded DataFrames
    data = pd.concat(data_frames, ignore_index=True)
    
    return data

# Function to load GeoJSON data
# @pn.cache
def load_geojson(file_path):
    """
    Load GeoJSON data from a given file path and cache it.
    """
    with open(file_path) as f:
        return json.load(f)

# Function to load GeoJSON data as a GeoDataFrame
# @pn.cache
def load_gdf(file_path):
    """
    Load GeoJSON data as a GeoDataFrame.
    """
    try:
        return gpd.read_file(file_path)
    except Exception as e:
        print(f"Error loading GeoJSON as DataFrame: {e}")
        return None

# Function to merge Europe GeoDataFrame with CSV data
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

# Function to rename columns to standardized format
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

        return data  # Return original data on error

# Function to convert columns to numeric and round values
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

# Function to convert country codes to standardized format
def remap_country_codes(data: pd.DataFrame, code_mapping: dict | None = None) -> pd.DataFrame:
    """
    Convert country codes in the DataFrame to standardized format.
    
    Args:
        data (pd.DataFrame): DataFrame with country codes to convert
        code_mapping (dict, optional): Custom mapping to override defaults
        
    Returns:
        pd.DataFrame: DataFrame with country codes converted
    """
    try:
        # Use centralized country code mapping if no custom mapping provided
        mapping = get_country_code_mapping(code_mapping) if code_mapping else get_country_code_mapping()
        
        if 'geo' in data.columns:
            data['geo'] = data['geo'].replace(mapping)
        if 'CNTR_ID' in data.columns:
            data['CNTR_ID'] = data['CNTR_ID'].replace(mapping)
        if 'Code' in data.columns:
            data['Code'] = data['Code'].replace(mapping)
        return data
    except Exception as e:
        print(f"Error converting country codes: {e}")
        return data  # Return original data on error

# Function to clean columns by removing unnecessary ones
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

# Function to add country flags using ISO2 codes
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
            data['ISO2_Code'] = data[code_column]
            data['Flag'] = data[code_column].apply(iso2_to_flag)
        return data
    except Exception as e:
        print(f"Error adding country flags: {e}")
        return data  # Return original data on error

# Function to apply energy type mappings
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

# Function to filter EU countries
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

