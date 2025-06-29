# tests/test_filters.py

import pytest
import pandas as pd
from data.filters import preprocess, filter_data

def test_preprocess_output_shape(raw_data):
    df, gdf = raw_data
    merged = preprocess(df, gdf)
    assert not merged.empty
    assert set(['Country', 'Code', 'Flag', 'Energy Type']).issubset(merged.columns)
    assert merged['Renewable Percentage'].between(0, 100).all()

def test_filter_data_eu_only(raw_data):
    df, gdf = raw_data
    merged = preprocess(df, gdf)
    df_renewable, df_eu_total = filter_data(merged)
    assert not df_renewable.empty
    assert not df_eu_total.empty
    assert df_renewable['Code'].nunique() <= 27
    assert df_eu_total['Year'].between(2004, 2022).all()