# data/filters.py

import pandas as pd
from utils.pd_helpers import (
    merge_data, rename_columns, clean_columns, 
    convert_data_types, remap_country_codes, add_country_flags,
    apply_energy_type_mapping, filter_eu_countries
)

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
    merged = apply_energy_type_mapping(merged)
    
    # Clean columns by dropping unnecessary ones
    merged = clean_columns(merged)
    
    # Convert data types and round values
    merged = convert_data_types(merged, ['Year', 'Renewable Percentage'])
    
    # Remap country codes (EL to GR for Greece)
    merged = remap_country_codes(merged)
    
    # Add country flags
    merged = add_country_flags(merged)
    
    return merged

# Filter the data for EU countries and calculate average renewable percentage
def filter_data(merged):
    """Filter data for EU countries and calculate average renewable percentage."""
    df_renewable = filter_eu_countries(merged)
    df_renewable = df_renewable[df_renewable['Energy Type'] == 'Renewable Energy Total']
    df_eu_total = df_renewable.groupby('Year', as_index=False)['Renewable Percentage'].mean().reset_index()
    return df_renewable, df_eu_total