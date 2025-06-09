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

# Main function to load and preprocess data

def load_data(
    data_path: str = './data/nrg_ind_ren_linear.csv',
    geo_path: str = './geo/europe.geojson',
    return_raw: bool = False
) -> Union[pd.DataFrame, Tuple[pd.DataFrame, gpd.GeoDataFrame]]:
    if not os.path.exists(data_path) or not os.path.exists(geo_path):
        raise FileNotFoundError("Missing input data files.")

    data = pd.read_csv(data_path)
    europe_gdf = gpd.read_file(geo_path)

    if return_raw:
        return data, europe_gdf

    merged_data = europe_gdf.merge(data, left_on='CNTR_ID', right_on='geo')

    merged_data.rename(columns={
        'nrg_bal': 'Energy Type', 'TIME_PERIOD': 'Year',
        'OBS_VALUE': 'Renewable Percentage', 'geo': 'Code',
        'NAME_ENGL': 'Country'
    }, inplace=True)

    energy_type_map = {
        'REN': 'Renewable Energy Total',
        'REN_ELC': 'Renewable Electricity',
        'REN_HEAT_CL': 'Renewable Heating and Cooling',
        'REN_TRA': 'Renewable Energy in Transport'
    }
    merged_data['Energy Type'] = merged_data['Energy Type'].replace(energy_type_map)

    merged_data.drop(columns=['LAST UPDATE', 'freq', 'unit', 'OBS_FLAG'], inplace=True)
    merged_data[['Year', 'Renewable Percentage']] = merged_data[['Year', 'Renewable Percentage']].apply(pd.to_numeric)
    merged_data['Renewable Percentage'] = merged_data['Renewable Percentage'].round(1)
    merged_data['Flag'] = merged_data['Code'].apply(iso2_to_flag)

    final_columns = [
        'Code', 'Flag', 'Country', 'Energy Type', 'Renewable Percentage', 'Year',
        'CNTR_ID', 'ISO3_CODE', 'geometry'
    ]
    return merged_data[final_columns]