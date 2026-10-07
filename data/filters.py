# data/filters.py

from typing import Union
import pandas as pd
import geopandas as gpd

from utils.helpers import (
    build_country_mapping,
    map_geo_keys,
    merge_data,
    rename_columns,
    apply_energy_type_mapping,
    clean_columns,
    convert_data_types,
    add_code_column,
    deduplicate_rows,
    add_iso2_code_column,
    add_country_flags,
    filter_by_energy_type,
    filter_eu_countries,
    calculate_eu_average,
)


def preprocess(data: pd.DataFrame, europe: Union[pd.DataFrame, gpd.GeoDataFrame]) -> pd.DataFrame:
    '''
    Function to preprocess the energy data.
    Merges the energy data with Europe GeoDataFrame, renames columns, and formats the data.
    '''
    country_mapping = build_country_mapping(europe)
    data = map_geo_keys(data, country_mapping)
    merged = merge_data(europe, data, left_key='CNTR_ID', right_key='geo_key')
    merged = rename_columns(merged)
    merged = apply_energy_type_mapping(merged)
    merged = clean_columns(merged)
    merged = convert_data_types(merged, ['Year', 'Renewable Percentage'])
    merged = add_code_column(merged, source_col='CNTR_ID', target_col='Code')
    merged = deduplicate_rows(merged, subset=['Code', 'Year', 'Energy Type'], keep='last')
    merged = add_iso2_code_column(merged, source_column='Code', target_column='ISO2_Code')
    merged = add_country_flags(merged)
    return merged


def filter_data(merged: pd.DataFrame) -> tuple[pd.DataFrame, pd.DataFrame]:
    '''
    Filter the data for EU countries and calculate average renewable percentage.
    '''
    df_renewable = filter_by_energy_type(merged, energy_type='Renewable Energy Total')
    df_renewable = filter_eu_countries(df_renewable, code_column='Code')
    df_renewable = deduplicate_rows(df_renewable, subset=['Code', 'Year'], keep='last')
    df_eu_total = calculate_eu_average(df_renewable, group_by='Year', target_col='Renewable Percentage')
    return df_renewable, df_eu_total