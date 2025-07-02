# data/loader.py

# Import necessary libraries

# Standard libraries os for file handling, typing for type hints
import os
from typing import Union, Tuple

# Pandas for data manipulation, GeoPandas for geographic data handling
import pandas as pd

# GeoPandas for geographic data handling
import geopandas as gpd

# Import configuration settings from config module
from config import (
    COLUMN_MAPPING,
    EU_COUNTRIES,
    COLUMNS_TO_DROP
)

# Custom utility function to convert ISO2 country code to flag emoji
from utils.flags import iso2_to_flag

# Import utility functions for data processing
from utils.helpers import merge_data, convert_data_types, clean_columns, add_iso2_code_column, add_iso2_code_columns

# Import mapping functions for column and energy type mappings
from utils.mapping import apply_column_mapping, apply_energy_type_mapping

# Define the main function to load and preprocess renewable energy data for Europe
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

    # Load the data from CSV and GeoJSON files  
    data = pd.read_csv(data_path)
    europe_gdf = gpd.read_file(geo_path)

    if return_raw:
        return data, europe_gdf
    
    # Add ISO2_CODE columns for flag purposes (EL→GR conversion)
    europe_gdf, data = add_iso2_code_columns(europe_gdf, data)

    # Merge the geographic data with the renewable energy data
    # merged_data = europe_gdf.merge(data, left_on='CNTR_ID', right_on='geo')
    merged_data = merge_data(europe_gdf, data, left_key='CNTR_ID', right_key='geo')

    # Rename columns for clarity
    # merged_data.rename(columns={
    #     'nrg_bal': 'Energy Type', 'TIME_PERIOD': 'Year',
    #     'OBS_VALUE': 'Renewable Percentage', 'geo': 'Code',
    #     'NAME_ENGL': 'Country'
    # }, inplace=True)
    merged_data = apply_column_mapping(merged_data, custom_mapping=COLUMN_MAPPING)

    # Map energy types to more descriptive names
    # energy_type_map = {
    #     'REN': 'Renewable Energy Total',
    #     'REN_ELC': 'Renewable Electricity',
    #     'REN_HEAT_CL': 'Renewable Heating and Cooling',
    #     'REN_TRA': 'Renewable Energy in Transport'
    # }
    # merged_data['Energy Type'] = merged_data['Energy Type'].replace(energy_type_map)
    merged_data = apply_energy_type_mapping(merged_data)

    # Drop unnecessary columns
    # merged_data.drop(columns=['LAST UPDATE', 'freq', 'unit', 'OBS_FLAG'], inplace=True)
    merged_data = clean_columns(merged_data)
   
    # Convert Year and Renewable Percentage to numeric and round
    merged_data = convert_data_types(merged_data, columns=['Year', 'Renewable Percentage'])
    # merged_data[['Year', 'Renewable Percentage']] = merged_data[['Year', 'Renewable Percentage']].apply(pd.to_numeric)
    # merged_data['Renewable Percentage'] = merged_data['Renewable Percentage'].round(1)

    # Add ISO2_Code for flag purposes (EL→GR), but keep Code as EL for plotting
    merged_data = add_iso2_code_column(merged_data)

    # Define the final columns to return
    final_columns = [
        'Code', 'Flag', 'Country', 'Energy Type', 'Renewable Percentage', 'Year',
        'CNTR_ID', 'ISO2_Code', 'ISO3_CODE', 'geometry'
    ]
    return merged_data[final_columns]