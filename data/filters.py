# data/filters.py

import pandas as pd
from utils.flags import iso2_to_flag
from utils.helpers import merge_data, rename_columns
from utils.mapping import ENERGY_TYPE_MAPPING

# Preprocess the data to merge with Europe GeoDataFrame and clean up columns

def preprocess(data: pd.DataFrame, europe: pd.DataFrame) -> pd.DataFrame:
    """
    Function to preprocess the energy data.
    Merges the energy data with Europe GeoDataFrame, renames columns, and formats the data.
    """
    # Merge the energy data with Europe GeoDataFrame
    merged = merge_data(europe, data, 'CNTR_ID', 'geo')
    # Rename columns to standardized format
    merged = rename_columns(merged)
    # Replace energy type codes with human-readable names
    merged['Energy Type'] = merged['Energy Type'].replace(ENERGY_TYPE_MAPPING)
    # Drop unnecessary columns
    merged.drop(columns=['LAST UPDATE', 'freq', 'unit', 'OBS_FLAG'], inplace=True)
    merged[['Year', 'Renewable Percentage']] = merged[['Year', 'Renewable Percentage']].apply(pd.to_numeric)
    merged['Renewable Percentage'] = merged['Renewable Percentage'].round(1)
    # Remap 'HL' (used for Greece in some datasets) to 'GR' to ensure correct merging
    merged['CNTR_ID'] = merged['CNTR_ID'].replace('EL', 'GR')
    merged['Code'] = merged['Code'].replace('EL', 'GR')
    merged['Flag'] = merged['Code'].apply(iso2_to_flag)
    return merged

# Filter the data for EU countries and calculate average renewable percentage
def filter_data(merged):
    """Filter data for EU countries and calculate average renewable percentage."""
    eu_countries = {"AT", "BE", "BG", "HR", "CY", "CZ", "DK", "EE", "FI", "FR", "DE", "GR", "HU", "IE", "IT", "LV", "LT",
                    "LU", "MT", "NL", "PL", "PT", "RO", "SK", "SI", "ES", "SE"}
    df_renewable = merged[(merged['Energy Type'] == 'Renewable Energy Total') & merged['Code'].isin(eu_countries)]
    df_eu_total = df_renewable.groupby('Year', as_index=False)['Renewable Percentage'].mean().reset_index()
    return df_renewable, df_eu_total