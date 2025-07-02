# data/filters.py

import pandas as pd
from utils.flags import add_country_flags
from utils.helpers import merge_data, convert_data_types, clean_columns, filter_eu_countries, add_iso2_code_column
from utils.mapping import apply_column_mapping, apply_energy_type_mapping, get_eu_countries
from config import COLUMN_MAPPING

# Preprocess the data to merge with Europe GeoDataFrame and clean up columns

def preprocess(data: pd.DataFrame, europe: pd.DataFrame) -> pd.DataFrame:
    '''
    Function to preprocess the energy data.
    Merges the energy data with Europe GeoDataFrame, renames columns, and formats the data.
    '''
    # Merge the energy data with Europe GeoDataFrame
    merged = merge_data(europe, data, left_key='CNTR_ID', right_key='geo')
    
    # Rename columns to standardized format using config mapping
    merged = apply_column_mapping(merged, custom_mapping=COLUMN_MAPPING)
    
    # Map energy types to more descriptive names
    merged = apply_energy_type_mapping(merged)
    
    # Drop unnecessary columns using helper function
    merged = clean_columns(merged)
    
    # Convert Year and Renewable Percentage to numeric and round
    merged = convert_data_types(merged, columns=['Year', 'Renewable Percentage'])
    
    # Add ISO2_Code for flag purposes (EL→GR), but keep Code as EL for plotting
    merged = add_iso2_code_column(merged)
    
    # Add country flags based on ISO2_Code
    merged = add_country_flags(merged)
    return merged

# Filter the data for EU countries and calculate average renewable percentage
def filter_data(merged: pd.DataFrame) -> tuple[pd.DataFrame, pd.DataFrame]:
    # Filter for renewable energy total and EU countries using helper function
    df_renewable = merged[merged['Energy Type'] == 'Renewable Energy Total']
    df_renewable = filter_eu_countries(df_renewable, code_column='Code')
    
    # Calculate EU average renewable percentage by year
    df_eu_total = df_renewable.groupby('Year', as_index=False)['Renewable Percentage'].mean().reset_index()
    return df_renewable, df_eu_total