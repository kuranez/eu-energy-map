# data/loader.py

import os
import pandas as pd
import geopandas as gpd

# def load_energy_data(path_data, path_geo):
#     data = pd.read_csv(path_data)
#     europe = gpd.read_file(path_geo)
#     return data, europe

def iso2_to_flag(iso2_code: str) -> str:
    return chr(0x1F1E6 + ord(iso2_code[0]) - ord('A')) + chr(0x1F1E6 + ord(iso2_code[1]) - ord('A'))

def load_data(data_path='./data/nrg_ind_ren_linear.csv', geo_path='./geo/europe.geojson') -> pd.DataFrame:
    if not os.path.exists(data_path) or not os.path.exists(geo_path):
        raise FileNotFoundError("Missing input data files.")

    data = pd.read_csv(data_path)
    europe_gdf = gpd.read_file(geo_path)

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
