# tests/test_loader.py

import os
import pytest
import pandas as pd
from data.loader import load_data, iso2_to_flag

@pytest.mark.usefixtures("raw_data")
def test_files_exist():
    assert os.path.exists('./data/nrg_ind_ren_linear.csv'), "CSV file missing."
    assert os.path.exists('./geo/europe.geojson'), "GeoJSON file missing."

def test_load_data_success():
    df = load_data()
    assert isinstance(df, pd.DataFrame)
    assert not df.empty, "Merged data should not be empty."
    assert 'Flag' in df.columns
    assert 'Renewable Percentage' in df.columns
    assert df['Renewable Percentage'].between(0, 100).all()

@pytest.mark.parametrize("iso2,flag", [
    ("DE", "🇩🇪"),
    ("FR", "🇫🇷"),
    ("SE", "🇸🇪"),
])
def test_iso2_to_flag(iso2, flag):
    assert iso2_to_flag(iso2) == flag

