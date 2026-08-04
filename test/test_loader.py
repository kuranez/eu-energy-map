# tests/test_loader.py

import os
import pytest
import pandas as pd
from data.loader import load_data, iso2_to_flag
from data.filters import filter_data
from components.charts.bar_chart_by_country import create_bar_chart_country

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


def test_load_data_includes_older_years_from_legacy_file(tmp_path):
    legacy_file = tmp_path / 'legacy.csv'

    pd.DataFrame([
        {'DATAFLOW': 'a', 'LAST UPDATE': 'x', 'freq': 'Annual', 'nrg_bal': 'REN', 'unit': 'PC', 'geo': 'DE', 'TIME_PERIOD': 2004, 'OBS_VALUE': 6.2, 'OBS_FLAG': '', 'CONF_STATUS': ''},
        {'DATAFLOW': 'a', 'LAST UPDATE': 'x', 'freq': 'Annual', 'nrg_bal': 'REN', 'unit': 'PC', 'geo': 'FR', 'TIME_PERIOD': 2004, 'OBS_VALUE': 9.3, 'OBS_FLAG': '', 'CONF_STATUS': ''},
    ]).to_csv(legacy_file, index=False)

    data, _ = load_data(data_path=[str(legacy_file)], geo_path='./geo/europe.geojson', return_raw=True)

    assert data['TIME_PERIOD'].min() == 2004
    assert data['nrg_bal'].eq('Renewable energy - overall').all()


def test_filter_data_deduplicates_country_year_rows():
    merged = pd.DataFrame({
        'Country': ['Germany', 'Germany'],
        'Code': ['DE', 'DE'],
        'Year': [2020, 2020],
        'Renewable Percentage': [20.0, 20.0],
        'Energy Type': ['Renewable Energy Total', 'Renewable Energy Total'],
    })

    df_renewable, df_eu_total = filter_data(merged)

    assert len(df_renewable) == 1
    assert df_eu_total['Renewable Percentage'].tolist() == [20.0]


def test_country_chart_range_follows_available_years():
    df_eu_total = pd.DataFrame({
        'Year': [2004, 2005, 2024],
        'Renewable Percentage': [10.0, 11.0, 20.0],
    })
    df_country = pd.DataFrame({
        'Year': [2004, 2005, 2024],
        'Renewable Percentage': [8.0, 9.0, 18.0],
        'Country': ['Germany'],
        'Flag': ['🇩🇪'],
    })

    fig = create_bar_chart_country(df_eu_total, df_country, 'Germany')

    assert fig.layout.xaxis.range == [2003.5, 2024.5]

@pytest.mark.parametrize("iso2,flag", [
    ("DE", "🇩🇪"),
    ("FR", "🇫🇷"),
    ("SE", "🇸🇪"),
])
def test_iso2_to_flag(iso2, flag):
    assert iso2_to_flag(iso2) == flag

