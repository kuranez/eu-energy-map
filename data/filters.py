# data/filters.py

import pandas as pd
from utils.flags import iso2_to_flag
from utils.helpers import merge_data, rename_columns

# Preprocess the data to merge with Europe GeoDataFrame and clean up columns

def preprocess(data: pd.DataFrame, europe: pd.DataFrame) -> pd.DataFrame:
    merged = merge_data(europe, data, 'CNTR_ID', 'geo')
    merged = rename_columns(merged)
    energy_type_map = {
        'REN': 'Renewable Energy Total',
        'REN_ELC': 'Renewable Electricity',
        'REN_HEAT_CL': 'Renewable Heating and Cooling',
        'REN_TRA': 'Renewable Energy in Transport'
    }
    merged['Energy Type'] = merged['Energy Type'].replace(energy_type_map)
    merged.drop(columns=['LAST UPDATE', 'freq', 'unit', 'OBS_FLAG'], inplace=True)
    merged[['Year', 'Renewable Percentage']] = merged[['Year', 'Renewable Percentage']].apply(pd.to_numeric)
    merged['Renewable Percentage'] = merged['Renewable Percentage'].round(1)
    # Remap 'HL' (used for Greece in some datasets) to 'GR' to ensure correct merging
    merged['CNTR_ID'] = merged['CNTR_ID'].replace('EL', 'GR')
    merged['Code'] = merged['Code'].replace('EL', 'GR')
    merged['Flag'] = merged['Code'].apply(iso2_to_flag)
    return merged

# Filter the data for EU countries and calculate average renewable percentage
def filter_data(merged: pd.DataFrame) -> tuple[pd.DataFrame, pd.DataFrame]:
    eu_countries = {"AT", "BE", "BG", "HR", "CY", "CZ", "DK", "EE", "FI", "FR", "DE", "EL", "HU", "IE", "IT", "LV", "LT",
                    "LU", "MT", "NL", "PL", "PT", "RO", "SK", "SI", "ES", "SE"}
    df_renewable = merged[(merged['Energy Type'] == 'Renewable Energy Total') & merged['Code'].isin(eu_countries)]
    df_eu_total = df_renewable.groupby('Year', as_index=False)['Renewable Percentage'].mean().reset_index()
    return df_renewable, df_eu_total