# tests/conftest.py

import pytest
import pandas as pd
import geopandas as gpd

@pytest.fixture(scope="module")
def raw_data():
    df = pd.read_csv('./data/nrg_ind_ren_linear.csv')
    gdf = gpd.read_file('./geo/europe.geojson')
    return df, gdf