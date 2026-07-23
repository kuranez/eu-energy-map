# data/loader.py

# Import necessary libraries

# Standard libraries os for file handling, typing for type hints
import os
from typing import Union, Tuple

# Pandas for data manipulation, GeoPandas for geographic data handling
import pandas as pd

# GeoPandas for geographic data handling
import geopandas as gpd

# Custom utility function to convert ISO2 country code to flag emoji
from utils.flags import iso2_to_flag


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
    
    # Merge the geographic data with the renewable energy data on country name
    merged_data = europe_gdf.merge(data, left_on='NAME_ENGL', right_on='geo')

    # Rename columns for clarity
    merged_data.rename(columns={
        'nrg_bal': 'Energy Type', 'TIME_PERIOD': 'Year',
        'OBS_VALUE': 'Renewable Percentage',
        'NAME_ENGL': 'Country'
    }, inplace=True)

    # Map energy types to more descriptive names
    energy_type_map = {
        'Renewable energy - overall': 'Renewable Energy Total',
        'Renewable energy - electricity': 'Renewable Electricity',
        'Renewable energy - heating and cooling': 'Renewable Heating and Cooling',
        'Renewable energy - transport': 'Renewable Energy in Transport'
    }
    merged_data['Energy Type'] = merged_data['Energy Type'].replace(energy_type_map)
    
    # Drop unnecessary columns
    columns_to_drop = ['DATAFLOW', 'LAST UPDATE', 'freq', 'unit', 'OBS_FLAG', 'CONF_STATUS', 'geo']
    merged_data.drop(columns=columns_to_drop, inplace=True, errors='ignore')
   
    # Convert Year and Renewable Percentage to numeric and round
    merged_data[['Year', 'Renewable Percentage']] = merged_data[['Year', 'Renewable Percentage']].apply(pd.to_numeric)
    merged_data['Renewable Percentage'] = merged_data['Renewable Percentage'].round(1)

    # Add 'Code' column from 'CNTR_ID' for plotting
    merged_data['Code'] = merged_data['CNTR_ID']
    
    # Add ISO2_Code for flag purposes (EL→GR), but keep Code as EL for plotting
    merged_data['ISO2_Code'] = merged_data['Code'].replace('EL', 'GR')
    merged_data['Flag'] = merged_data['ISO2_Code'].apply(iso2_to_flag)

    # Define the final columns to return
    final_columns = [
        'Code', 'Flag', 'Country', 'Energy Type', 'Renewable Percentage', 'Year',
        'CNTR_ID', 'ISO2_Code', 'ISO3_CODE', 'geometry'
    ]
    return merged_data[final_columns]