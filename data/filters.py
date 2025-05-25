# data/filters.py

import pandas as pd

# Convert ISO2 country code to flag emoji

def iso2_to_flag(iso2_code: str) -> str:
    return chr(0x1F1E6 + ord(iso2_code[0]) - ord('A')) + chr(0x1F1E6 + ord(iso2_code[1]) - ord('A'))

# Preprocess the data to merge with Europe GeoDataFrame and clean up columns

def preprocess(data: pd.DataFrame, europe: pd.DataFrame) -> pd.DataFrame:
    merged = europe.merge(data, left_on='CNTR_ID', right_on='geo')
    merged.rename(columns={
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
    merged['Energy Type'] = merged['Energy Type'].replace(energy_type_map)
    merged.drop(columns=['LAST UPDATE', 'freq', 'unit', 'OBS_FLAG'], inplace=True)
    merged[['Year', 'Renewable Percentage']] = merged[['Year', 'Renewable Percentage']].apply(pd.to_numeric)
    merged['Renewable Percentage'] = merged['Renewable Percentage'].round(1)
    merged['Flag'] = merged['Code'].apply(iso2_to_flag)
    return merged

# Filter the data for EU countries and calculate average renewable percentage
def filter_data(merged: pd.DataFrame) -> tuple[pd.DataFrame, pd.DataFrame]:
    eu_countries = {"AT", "BE", "BG", "HR", "CY", "CZ", "DK", "EE", "FI", "FR", "DE", "EL", "HU", "IE", "IT", "LV", "LT",
                    "LU", "MT", "NL", "PL", "PT", "RO", "SK", "SI", "ES", "SE"}
    df_renewable = merged[(merged['Energy Type'] == 'Renewable Energy Total') & merged['Code'].isin(eu_countries)]
    df_eu_total = df_renewable.groupby('Year', as_index=False)['Renewable Percentage'].mean().reset_index()
    return df_renewable, df_eu_total