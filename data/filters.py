# data/filters.py

import pandas as pd
from utils.flags import add_country_flags

# Preprocess the data to merge with Europe GeoDataFrame and clean up columns

def preprocess(data: pd.DataFrame, europe: pd.DataFrame) -> pd.DataFrame:
    '''
    Function to preprocess the energy data.
    Merges the energy data with Europe GeoDataFrame, renames columns, and formats the data.
    '''
    # Merge the energy data with Europe GeoDataFrame
    merged = europe.merge(data, left_on='NAME_ENGL', right_on='geo')
    # Rename columns to standardized format
    merged.rename(columns={
        'nrg_bal': 'Energy Type', 'TIME_PERIOD': 'Year',
        'OBS_VALUE': 'Renewable Percentage',
        'NAME_ENGL': 'Country'
    }, inplace=True)
    # Replace energy type codes with human-readable names
    energy_type_map = {
        'Renewable energy - overall': 'Renewable Energy Total',
        'Renewable energy - electricity': 'Renewable Electricity',
        'Renewable energy - heating and cooling': 'Renewable Heating and Cooling',
        'Renewable energy - transport': 'Renewable Energy in Transport'
    }
    # Apply the energy type mapping
    merged['Energy Type'] = merged['Energy Type'].replace(energy_type_map)
    # Drop unnecessary columns
    columns_to_drop = ['DATAFLOW', 'LAST UPDATE', 'freq', 'unit', 'OBS_FLAG', 'CONF_STATUS', 'geo']
    merged.drop(columns=columns_to_drop, inplace=True, errors='ignore')
    # Convert Year and Renewable Percentage to numeric and round
    merged[['Year', 'Renewable Percentage']] = merged[['Year', 'Renewable Percentage']].apply(pd.to_numeric)
    # Round the Renewable Percentage
    merged['Renewable Percentage'] = merged['Renewable Percentage'].round(1)
    # Add 'Code' column from 'CNTR_ID' for plotting
    merged['Code'] = merged['CNTR_ID']
    # Add ISO2_Code for flag purposes (EL→GR), but keep Code as EL for plotting
    merged['ISO2_Code'] = merged['Code'].replace('EL', 'GR')
    # Add country flags based on ISO2_Code
    merged = add_country_flags(merged)
    return merged

# Filter the data for EU countries and calculate average renewable percentage
def filter_data(merged: pd.DataFrame) -> tuple[pd.DataFrame, pd.DataFrame]:
    eu_countries = {"AT", "BE", "BG", "HR", "CY", "CZ", "DK", "EE", "FI", "FR", "DE", "EL", "HU", "IE", "IT", "LV", "LT",
                    "LU", "MT", "NL", "PL", "PT", "RO", "SK", "SI", "ES", "SE"}
    df_renewable = merged[(merged['Energy Type'] == 'Renewable Energy Total') & merged['Code'].isin(eu_countries)]
    df_eu_total = df_renewable.groupby('Year', as_index=False)['Renewable Percentage'].mean().reset_index()
    return df_renewable, df_eu_total