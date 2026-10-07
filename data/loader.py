# data/loader.py

# Standard libraries os for file handling, typing for type hints
import os
from typing import Union, Tuple, Sequence

# Pandas and GeoPandas type hints
import pandas as pd
import geopandas as gpd

# Helper functions from utils.helpers
from utils.helpers import (
    load_csv_data,
    load_gdf,
    normalize_frame_columns,
    build_country_mapping,
    map_geo_keys,
    concat_dataframes,
    merge_data,
    rename_columns,
    apply_energy_type_mapping,
    clean_columns,
    convert_data_types,
    add_code_column,
    add_iso2_code_column,
    add_country_flags,
    select_columns,
    iso2_to_flag,
)


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

    europe_gdf = load_gdf(geo_path)
    data_frames = []
    country_mapping = build_country_mapping(europe_gdf)

    for path in data_paths:
        frame = load_csv_data(path)
        frame = normalize_frame_columns(frame)
        frame = map_geo_keys(frame, country_mapping)
        data_frames.append(frame)

    data = concat_dataframes(data_frames)

    if return_raw:
        return data, europe_gdf

    merged_data = merge_data(europe_gdf, data, left_key='CNTR_ID', right_key='geo_key')
    merged_data = rename_columns(merged_data)
    merged_data = apply_energy_type_mapping(merged_data)
    merged_data = clean_columns(merged_data)
    merged_data = convert_data_types(merged_data, ['Year', 'Renewable Percentage'])
    merged_data = add_code_column(merged_data, source_col='CNTR_ID', target_col='Code')
    merged_data = add_iso2_code_column(merged_data, source_column='Code', target_column='ISO2_Code')
    merged_data = add_country_flags(merged_data)

    return select_columns(merged_data)