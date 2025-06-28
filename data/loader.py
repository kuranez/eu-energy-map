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
from utils.flags import iso2_to_flag
from utils.helpers import load_csv_data, load_gdf, merge_data, rename_columns
from utils.mapping import ENERGY_TYPE_MAPPING

# Main function to load and preprocess data

def load_data(
    data_path: str = './data/nrg_ind_ren_linear.csv',
    geo_path: str = './geo/europe.geojson',
    return_raw: bool = False
) -> Union[pd.DataFrame, Tuple[pd.DataFrame, gpd.GeoDataFrame]]:
    if not os.path.exists(data_path) or not os.path.exists(geo_path):
        raise FileNotFoundError("Missing input data files.")

    data = load_csv_data(data_path)
    europe_gdf = load_gdf(geo_path)
    
    # Check if loading was successful
    if data is None or europe_gdf is None:
        raise RuntimeError("Failed to load input data files.")

    if return_raw:
        return data, europe_gdf

    merged_data = merge_data(europe_gdf, data, 'CNTR_ID', 'geo')

    merged_data = rename_columns(merged_data)

    merged_data['Energy Type'] = merged_data['Energy Type'].replace(ENERGY_TYPE_MAPPING)

    merged_data.drop(columns=['LAST UPDATE', 'freq', 'unit', 'OBS_FLAG'], inplace=True)
    merged_data[['Year', 'Renewable Percentage']] = merged_data[['Year', 'Renewable Percentage']].apply(pd.to_numeric)
    merged_data['Renewable Percentage'] = merged_data['Renewable Percentage'].round(1)
    # Remap 'HL' (used for Greece in some datasets) to 'GR' to ensure correct merging
    merged_data['CNTR_ID'] = merged_data['CNTR_ID'].replace('EL', 'GR')
    merged_data['Code'] = merged_data['Code'].replace('EL', 'GR')
    merged_data['Flag'] = merged_data['Code'].apply(iso2_to_flag)

    final_columns = [
        'Code', 'Flag', 'Country', 'Energy Type', 'Renewable Percentage', 'Year',
        'CNTR_ID', 'ISO3_CODE', 'geometry'
    ]
    return merged_data[final_columns]