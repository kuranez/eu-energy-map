# utils/helpers.py
import os
import glob
import json
import pandas as pd
import geopandas as gpd
# import panel as pn  # Assuming you are using Panel for caching

# Method List:
# 1. load_csv_data: Simple CSV loading function
# 2. load_and_combine_csv_data: Enhanced CSV loading function that combines multiple files  
# 3. load_geojson: Function to load GeoJSON data
# 4. load_gdf: Function to load GeoJSON data as a GeoDataFrame
# 5. merge_data: Function to merge Europe GeoDataFrame with CSV data
# 6. rename_columns: Function to rename columns to standardized format

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
    # Default column mapping
    default_mapping = {
        'nrg_bal': 'Energy Type',
        'TIME_PERIOD': 'Year',
        'OBS_VALUE': 'Renewable Percentage',
        'geo': 'Code',
        'NAME_ENGL': 'Country'
    }
    
    # Use custom mapping if provided, otherwise use default
    column_mapping = custom_mapping if custom_mapping else default_mapping
    
    try:
        # Create a copy to avoid modifying original data
        renamed_data = data.copy()
        renamed_data.rename(columns=column_mapping, inplace=True)
        return renamed_data
    except Exception as e:
        print(f"Error renaming columns: {e}")
        return data  # Return original data on error