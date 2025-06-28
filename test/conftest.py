# tests/conftest.py

import pytest
import pandas as pd
import geopandas as gpd
import os

@pytest.fixture(scope="module")
def raw_data():
    """Load raw CSV and GeoJSON data for testing."""
    df = pd.read_csv('./data/nrg_ind_ren_linear.csv')
    gdf = gpd.read_file('./geo/europe.geojson')
    return df, gdf

@pytest.fixture(scope="module")
def sample_csv_data():
    """Create sample CSV data for testing."""
    return pd.DataFrame({
        'geo': ['DE', 'FR', 'EL'],
        'nrg_bal': ['REN', 'REN_ELC', 'REN_HEAT_CL'],
        'TIME_PERIOD': [2020, 2021, 2022],
        'OBS_VALUE': [25.5, 30.2, 15.8],
        'LAST UPDATE': ['2023-01-01', '2023-01-01', '2023-01-01'],
        'freq': ['A', 'A', 'A'],
        'unit': ['PC', 'PC', 'PC'],
        'OBS_FLAG': ['', '', '']
    })

@pytest.fixture(scope="module")
def sample_geo_data():
    """Create sample GeoJSON data for testing."""
    return gpd.GeoDataFrame({
        'CNTR_ID': ['DE', 'FR', 'GR'],
        'NAME_ENGL': ['Germany', 'France', 'Greece'],
        'ISO3_CODE': ['DEU', 'FRA', 'GRC'],
        'geometry': [None, None, None]  # Simplified for testing
    })