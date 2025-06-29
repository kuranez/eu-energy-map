# utils/helpers.py
import os
import glob
import json
import pandas as pd
import geopandas as gpd
# import panel as pn  # Assuming you are using Panel for caching

from utils.mapping import get_columns_to_drop, get_eu_countries

# Method List:
# 1. load_csv_data: Simple CSV loading function
# 2. load_and_combine_csv_data: Enhanced CSV loading function that combines multiple files  
# 3. load_geojson: Function to load GeoJSON data
# 4. load_gdf: Function to load GeoJSON data as a GeoDataFrame
# 5. merge_data: Function to merge Europe GeoDataFrame with CSV data
# 6. convert_data_types: Function to convert specified columns to numeric and round values
# 7. clean_columns: Function to clean the DataFrame by dropping unnecessary columns
# 8. filter_eu_countries: Function to filter DataFrame to include only EU

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

# Function to convert specified columns to numeric and round values
# @pn.cache
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

# Function to clean the DataFrame by dropping unnecessary columns
# @pn.cache
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