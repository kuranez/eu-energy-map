# data/loader.py

# Import necessary libraries

# Standard libraries os for file handling, typing for type hints
import os
from typing import Union, Tuple

# Pandas for data manipulation, GeoPandas for geographic data handling
import pandas as pd

# GeoPandas for geographic data handling
import geopandas as gpd

# Custom utility functions
from utils.helpers import load_csv_data, load_gdf
from utils.pd_helpers import (
    merge_data, rename_columns, clean_columns, convert_data_types, 
    remap_country_codes, add_country_flags, apply_energy_type_mapping
)

# Main function to load and preprocess data

def load_data(
    data_path: str = './data/nrg_ind_ren_linear.csv',
    geo_path: str = './geo/europe.geojson',
    return_raw: bool = False
) -> Union[pd.DataFrame, Tuple[pd.DataFrame, gpd.GeoDataFrame]]:
    '''
    Main function to load and preprocess renewable energy data for Europe.
    Parameters:
    - data_path: Path to the renewable energy data CSV file.
    - geo_path: Path to the geographic data GeoJSON file.
    - return_raw: If True, returns raw data without processing.
    Returns:
    - If return_raw is True, returns a tuple of (data, europe_gdf).
    - Otherwise, returns a processed DataFrame with renewable energy data.
    '''
    # Check if the input data files exist
    if not os.path.exists(data_path) or not os.path.exists(geo_path):
        # Raise an error if files are missing
        raise FileNotFoundError("Missing input data files.")

    data = load_csv_data(data_path)
    europe_gdf = load_gdf(geo_path)
    
    # Check if loading was successful
    if data is None or europe_gdf is None:
        raise RuntimeError("Failed to load input data files.")

    if return_raw:
        return data, europe_gdf
    
    # Add ISO2_CODE column, replacing 'EL' with 'GR' for flag purposes
    europe_gdf['ISO2_CODE'] = europe_gdf['CNTR_ID'].replace('EL', 'GR')
    data['ISO2_CODE'] = data['geo'].replace('EL', 'GR')
    
    # First merge the data using original country codes (before remapping)
    merged_data = merge_data(europe_gdf, data, 'CNTR_ID', 'geo')

    # Handle duplicate ISO2_CODE columns (keep the one from geo data)
    if 'ISO2_CODE_x' in merged_data.columns and 'ISO2_CODE_y' in merged_data.columns:
        merged_data['ISO2_CODE'] = merged_data['ISO2_CODE_x']  # Use geo data version
        merged_data = merged_data.drop(columns=['ISO2_CODE_x', 'ISO2_CODE_y'])

    merged_data = rename_columns(merged_data)

    merged_data = apply_energy_type_mapping(merged_data)

    merged_data = clean_columns(merged_data)
    merged_data = convert_data_types(merged_data, ['Year', 'Renewable Percentage'])
    
    # Apply country code remapping AFTER merging (for display purposes)
    merged_data = remap_country_codes(merged_data)

    # Add country flags using ISO2_CODE column (which has EL→GR mapping for Greece)
    merged_data = add_country_flags(merged_data, code_column='ISO2_CODE')

    final_columns = [
        'Code', 'Flag', 'Country', 'Energy Type', 'Renewable Percentage', 'Year',
        'CNTR_ID', 'ISO2_CODE', 'geometry'
    ]
    return merged_data[final_columns]