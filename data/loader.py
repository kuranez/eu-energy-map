# data/loader.py

# Import necessary libraries

# Standard libraries os for file handling, typing for type hints
import os
from typing import Union, Tuple, Sequence

# Pandas for data manipulation, GeoPandas for geographic data handling
import pandas as pd

# GeoPandas for geographic data handling
import geopandas as gpd

# Custom utility function to convert ISO2 country code to flag emoji
from utils.flags import iso2_to_flag


def _normalize_frame_columns(frame: pd.DataFrame) -> pd.DataFrame:
    """Normalize Eurostat renewable datasets from different export formats."""
    frame = frame.copy()

    if 'nrg_bal' not in frame.columns and 'siec' in frame.columns:
        frame = frame.rename(columns={'siec': 'nrg_bal'})

    if 'nrg_bal' in frame.columns:
        frame['nrg_bal'] = frame['nrg_bal'].astype(str).str.strip()
        frame['nrg_bal'] = frame['nrg_bal'].replace({
            'REN': 'Renewable energy - overall',
            'R5110-5150_W6000RIS': 'Renewable energy - overall',
            'Renewable energy - overall': 'Renewable energy - overall',
        })

    if 'nrg_bal' not in frame.columns:
        frame['nrg_bal'] = 'Renewable energy - overall'

    if 'TIME_PERIOD' in frame.columns:
        frame['TIME_PERIOD'] = pd.to_numeric(frame['TIME_PERIOD'], errors='coerce')

    return frame


def load_data(
    data_path: Union[str, Sequence[str]] = (
        './data/nrg_ind_ren_linear.csv',
        './data/nrg_ind_ren_linear_old.csv',
    ),
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
    if isinstance(data_path, (str, os.PathLike)):
        data_paths = [str(data_path)]
    else:
        data_paths = [str(path) for path in data_path]

    if not all(os.path.exists(path) for path in data_paths) or not os.path.exists(geo_path):
        raise FileNotFoundError("Missing input data files.")

    europe_gdf = gpd.read_file(geo_path)
    data_frames = []

    for path in data_paths:
        frame = pd.read_csv(path)
        frame = _normalize_frame_columns(frame)

        country_mapping = {}
        for _, row in europe_gdf.iterrows():
            for value in [row.get('NAME_ENGL'), row.get('CNTR_ID'), row.get('ISO3_CODE'), row.get('ISO2_Code')]:
                if pd.notna(value):
                    country_mapping[str(value).strip()] = row['CNTR_ID']

        frame['geo_key'] = frame['geo'].astype(str).map(country_mapping).fillna(frame['geo']).astype(str)
        data_frames.append(frame)

    data = pd.concat(data_frames, ignore_index=True)

    if return_raw:
        return data, europe_gdf

    merged_data = europe_gdf.merge(data, left_on='CNTR_ID', right_on='geo_key')

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
    columns_to_drop = ['DATAFLOW', 'LAST UPDATE', 'freq', 'unit', 'OBS_FLAG', 'CONF_STATUS', 'geo', 'geo_key']
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