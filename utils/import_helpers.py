# utils/import_helpers.py

"""
Import and mapping utilities for EU Energy Map project.
Contains data loading functions and mapping constants/functions.
"""

import os
import glob
import json
import pandas as pd
import geopandas as gpd
# import panel as pn  # Assuming you are using Panel for caching

# =============================================================================
# MAPPING CONSTANTS AND FUNCTIONS
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
# DATA LOADING FUNCTIONS
# =============================================================================

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
