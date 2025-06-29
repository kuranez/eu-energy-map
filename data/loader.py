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
from utils.helpers import (
    load_csv_data, load_gdf, merge_data, rename_columns, 
    clean_columns, convert_data_types, remap_country_codes, add_country_flags,
    apply_energy_type_mapping
)

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
    
    merged_data = remap_country_codes(data)
    merged_data = merge_data(europe_gdf, merged_data, 'CNTR_ID', 'geo')

    merged_data = rename_columns(merged_data)

    merged_data = apply_energy_type_mapping(merged_data)

    merged_data = clean_columns(merged_data)
    merged_data = convert_data_types(merged_data, ['Year', 'Renewable Percentage'])

    merged_data = add_country_flags(merged_data)

    final_columns = [
        'Code', 'Flag', 'Country', 'Energy Type', 'Renewable Percentage', 'Year',
        'CNTR_ID', 'ISO3_CODE', 'geometry'
    ]
    return merged_data[final_columns]