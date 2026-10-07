# utils/helpers.py

"""
Helper functions for EU Energy Map project.
Encapsulates all direct Pandas and GeoPandas operations to provide
a clean, centralized interface for data loading, transformation, and filtering.
"""

import os
import glob
import json
from typing import Union, Sequence
import pandas as pd
import geopandas as gpd

from config import (
    COLUMN_MAPPING,
    COLUMNS_TO_DROP,
    ENERGY_TYPE_MAPPING,
    COUNTRY_CODE_MAPPING,
    EU_COUNTRIES,
    NORMALIZE_ENERGY_MAPPING,
    FINAL_COLUMNS,
)
from utils.mapping import (
    get_columns_to_drop,
    get_eu_countries,
    get_column_mapping,
    get_energy_type_mapping,
    get_country_code_mapping,
)


# =============================================================================
# 1. File & Data Loading Helpers
# =============================================================================

def load_csv_data(file_path: Union[str, os.PathLike]) -> pd.DataFrame:
    """
    Load CSV data from a given file path with low_memory=False to avoid dtype warnings.
    """
    try:
        return pd.read_csv(file_path, low_memory=False)
    except Exception as e:
        print(f"Error loading CSV '{file_path}': {e}")
        return pd.DataFrame()


def load_and_combine_csv_data(folder_path: Union[str, os.PathLike], pattern: str = "estat_nrg_cb_*.csv") -> pd.DataFrame:
    """
    Load and combine multiple CSV files from the specified folder matching a pattern.
    """
    csv_files = glob.glob(os.path.join(folder_path, pattern))
    data_frames = []
    for file in csv_files:
        df = load_csv_data(file)
        if not df.empty:
            data_frames.append(df)
    
    return concat_dataframes(data_frames)


def load_geojson(file_path: Union[str, os.PathLike]) -> dict:
    """
    Load GeoJSON data from a given file path.
    """
    with open(file_path, "r", encoding="utf-8") as f:
        return json.load(f)


def load_gdf(file_path: Union[str, os.PathLike]) -> gpd.GeoDataFrame:
    """
    Load GeoJSON or spatial data as a GeoDataFrame.
    """
    try:
        return gpd.read_file(file_path)
    except Exception as e:
        print(f"Error loading GeoDataFrame from '{file_path}': {e}")
        return gpd.GeoDataFrame()


def concat_dataframes(data_frames: Sequence[pd.DataFrame], ignore_index: bool = True) -> pd.DataFrame:
    """
    Concatenate a sequence of DataFrames into a single DataFrame.
    """
    if not data_frames:
        return pd.DataFrame()
    return pd.concat(data_frames, ignore_index=ignore_index)


# =============================================================================
# 2. Data Normalization & Mapping Helpers
# =============================================================================

def normalize_frame_columns(frame: pd.DataFrame, mapping: dict | None = None) -> pd.DataFrame:
    """
    Normalize Eurostat renewable datasets from different export formats.
    Standardizes 'siec'/'nrg_bal' columns and energy balance codes.
    """
    frame = frame.copy()

    if 'nrg_bal' not in frame.columns and 'siec' in frame.columns:
        frame = frame.rename(columns={'siec': 'nrg_bal'})

    norm_map = mapping if mapping is not None else NORMALIZE_ENERGY_MAPPING
    if 'nrg_bal' in frame.columns:
        frame['nrg_bal'] = frame['nrg_bal'].astype(str).str.strip()
        frame['nrg_bal'] = frame['nrg_bal'].replace(norm_map)
    else:
        frame['nrg_bal'] = 'Renewable energy - overall'

    if 'TIME_PERIOD' in frame.columns:
        frame['TIME_PERIOD'] = pd.to_numeric(frame['TIME_PERIOD'], errors='coerce')

    return frame


def build_country_mapping(europe_gdf: gpd.GeoDataFrame) -> dict[str, str]:
    """
    Build a mapping dictionary from various country identifiers
    (NAME_ENGL, CNTR_ID, ISO3_CODE, ISO2_Code) to the standard CNTR_ID.
    """
    country_mapping = {}
    for _, row in europe_gdf.iterrows():
        for key in ['NAME_ENGL', 'CNTR_ID', 'ISO3_CODE', 'ISO2_Code']:
            value = row.get(key)
            if pd.notna(value):
                country_mapping[str(value).strip()] = row['CNTR_ID']
    return country_mapping


def map_geo_keys(
    frame: pd.DataFrame,
    country_mapping: dict[str, str],
    source_col: str = 'geo',
    target_col: str = 'geo_key'
) -> pd.DataFrame:
    """
    Map geographic identifier in source_col to standardized CNTR_ID in target_col.
    """
    frame = frame.copy()
    if source_col in frame.columns:
        frame[target_col] = (
            frame[source_col]
            .astype(str)
            .map(country_mapping)
            .fillna(frame[source_col])
            .astype(str)
        )
    return frame


def rename_columns(data: pd.DataFrame, custom_mapping: dict | None = None) -> pd.DataFrame:
    """
    Standardize DataFrame column names using COLUMN_MAPPING from config.
    """
    mapping = get_column_mapping(custom_mapping)
    return data.rename(columns=mapping, errors='ignore')


def apply_energy_type_mapping(
    data: pd.DataFrame,
    custom_mapping: dict | None = None,
    column_name: str = 'Energy Type'
) -> pd.DataFrame:
    """
    Standardize energy type codes into descriptive names using ENERGY_TYPE_MAPPING from config.
    """
    if column_name in data.columns:
        data = data.copy()
        mapping = get_energy_type_mapping(custom_mapping)
        data[column_name] = data[column_name].replace(mapping)
    return data


def clean_columns(data: pd.DataFrame, columns_to_drop: list[str] | None = None) -> pd.DataFrame:
    """
    Drop unnecessary metadata columns using COLUMNS_TO_DROP from config.
    """
    columns = get_columns_to_drop(columns_to_drop)
    return data.drop(columns=columns, inplace=False, errors='ignore')


def convert_data_types(
    data: pd.DataFrame,
    columns: list[str] | None = None,
    round_digits: int = 1
) -> pd.DataFrame:
    """
    Convert specified columns to numeric and round float values.
    """
    data = data.copy()
    if columns is None:
        columns = ['Year', 'Renewable Percentage']
    
    for col in columns:
        if col in data.columns:
            data[col] = pd.to_numeric(data[col], errors='coerce')
            if col == 'Renewable Percentage' or (round_digits is not None and pd.api.types.is_float_dtype(data[col])):
                data[col] = data[col].round(round_digits)
    return data


def add_code_column(data: pd.DataFrame, source_col: str = 'CNTR_ID', target_col: str = 'Code') -> pd.DataFrame:
    """
    Duplicate/assign CNTR_ID as Code column for plotting convenience.
    """
    data = data.copy()
    if source_col in data.columns:
        data[target_col] = data[source_col]
    return data


def add_iso2_code_column(
    data: pd.DataFrame,
    source_column: str = 'Code',
    target_column: str = 'ISO2_Code',
    mapping: dict | None = None
) -> pd.DataFrame:
    """
    Add ISO2_Code column (mapping EL→GR for flag display) using COUNTRY_CODE_MAPPING from config.
    """
    data = data.copy()
    code_map = get_country_code_mapping(mapping)
    if source_column in data.columns:
        data[target_column] = data[source_column].replace(code_map)
    return data


def add_iso2_code_columns(
    europe_gdf: gpd.GeoDataFrame,
    data: pd.DataFrame,
    geo_source_col: str = 'CNTR_ID',
    data_source_col: str = 'geo',
    mapping: dict | None = None
) -> tuple[gpd.GeoDataFrame, pd.DataFrame]:
    """
    Add ISO2_CODE columns to both GeoDataFrame and DataFrame for flag purposes.
    """
    code_map = get_country_code_mapping(mapping)
    europe_gdf = europe_gdf.copy()
    data = data.copy()

    if geo_source_col in europe_gdf.columns:
        europe_gdf['ISO2_CODE'] = europe_gdf[geo_source_col].replace(code_map)
    if data_source_col in data.columns:
        data['ISO2_CODE'] = data[data_source_col].replace(code_map)

    return europe_gdf, data


# =============================================================================
# 3. Merging & Column Selection Helpers
# =============================================================================

def merge_data(
    europe: Union[pd.DataFrame, gpd.GeoDataFrame],
    data: pd.DataFrame,
    left_key: str = 'CNTR_ID',
    right_key: str = 'geo_key'
) -> Union[pd.DataFrame, gpd.GeoDataFrame]:
    """
    Merge Europe GeoDataFrame with CSV data on specified keys.
    """
    try:
        return europe.merge(data, left_on=left_key, right_on=right_key)
    except Exception as e:
        print(f"Error merging data: {e}")
        return pd.DataFrame()


def select_columns(data: pd.DataFrame, columns: list[str] | None = None) -> pd.DataFrame:
    """
    Filter DataFrame to return only specified columns (defaults to FINAL_COLUMNS from config).
    """
    cols = columns if columns is not None else FINAL_COLUMNS
    existing_cols = [col for col in cols if col in data.columns]
    return data[existing_cols]


# =============================================================================
# 4. Deduplication, Filtering & Aggregation Helpers
# =============================================================================

def deduplicate_rows(data: pd.DataFrame, subset: list[str], keep: str = 'last') -> pd.DataFrame:
    """
    Deduplicate DataFrame rows based on a subset of columns.
    """
    return data.drop_duplicates(subset=subset, keep=keep)


def filter_eu_countries(
    data: pd.DataFrame,
    code_column: str = 'Code',
    additional_countries: set | None = None
) -> pd.DataFrame:
    """
    Filter DataFrame to include only EU countries using EU_COUNTRIES from config.
    """
    eu_countries = get_eu_countries(additional_countries)
    if code_column in data.columns:
        return data[data[code_column].isin(eu_countries)]
    return data


def filter_by_energy_type(
    data: pd.DataFrame,
    energy_type: str = 'Renewable Energy Total',
    column: str = 'Energy Type'
) -> pd.DataFrame:
    """
    Filter DataFrame rows by energy type.
    """
    if column in data.columns:
        return data[data[column] == energy_type]
    return data


def calculate_eu_average(
    data: pd.DataFrame,
    group_by: str = 'Year',
    target_col: str = 'Renewable Percentage'
) -> pd.DataFrame:
    """
    Calculate average target_col grouped by group_by column.
    """
    return data.groupby(group_by, as_index=False)[target_col].mean().reset_index()


# =============================================================================
# 5. Flag Emoji Utilities (Moved from flags.py)
# =============================================================================

def iso2_to_flag(iso2_code: str) -> str:
    """
    Convert ISO2 country code to flag emoji.
    Example: 'DE' -> 🇩🇪
    
    Args:
        iso2_code (str): A two-letter ISO 3166-1 alpha-2 country code.
    
    Returns:
        str: The corresponding flag emoji or an empty string if invalid.
    """
    if not isinstance(iso2_code, str) or len(iso2_code) != 2:
        return ""
    return chr(0x1F1E6 + ord(iso2_code[0].upper()) - ord('A')) + chr(0x1F1E6 + ord(iso2_code[1].upper()) - ord('A'))


def add_country_flags(
    data: pd.DataFrame,
    source_column: str = 'ISO2_Code',
    target_column: str = 'Flag'
) -> pd.DataFrame:
    """
    Add national flag emojis to the DataFrame based on source_column.
    """
    data = data.copy()
    if source_column in data.columns:
        data[target_column] = data[source_column].apply(iso2_to_flag)
    return data
