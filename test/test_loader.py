# tests/test_loader.py

import os
import pytest
import pandas as pd
import geopandas as gpd
from data.loader import load_data
from utils.flags import iso2_to_flag

class TestDataLoader:
    """Test suite for data loading functionality."""
    
    @pytest.mark.usefixtures("raw_data")
    def test_files_exist(self):
        """Test that required data files exist."""
        assert os.path.exists('./data/nrg_ind_ren_linear.csv'), "CSV file missing."
        assert os.path.exists('./geo/europe.geojson'), "GeoJSON file missing."

    def test_load_data_success(self):
        """Test successful data loading and processing."""
        df = load_data()
        assert isinstance(df, pd.DataFrame)
        assert not df.empty, "Merged data should not be empty."
        assert 'Flag' in df.columns
        assert 'Renewable Percentage' in df.columns

    def test_load_data_return_raw(self):
        """Test loading raw data without processing."""
        result = load_data(return_raw=True)
        assert isinstance(result, tuple)
        data, gdf = result
        assert isinstance(data, pd.DataFrame)
        assert isinstance(gdf, gpd.GeoDataFrame)
        assert not data.empty
        assert len(gdf) > 0

    def test_load_data_file_not_found(self):
        """Test error handling for missing files."""
        with pytest.raises(FileNotFoundError):
            load_data(data_path='./nonexistent.csv')

    def test_load_data_columns(self):
        """Test that loaded data has expected basic columns."""
        df = load_data()
        assert isinstance(df, pd.DataFrame)
        expected_columns = ['Code', 'Flag', 'Country', 'Energy Type', 'Renewable Percentage', 'Year']
        for col in expected_columns:
            assert col in df.columns, f"Missing expected column: {col}"

    def test_load_data_energy_types(self):
        """Test that energy types are properly mapped."""
        df = load_data()
        assert isinstance(df, pd.DataFrame)
        energy_types = df['Energy Type'].unique()
        expected_types = [
            'Renewable Energy Total',
            'Renewable Electricity', 
            'Renewable Heating and Cooling',
            'Renewable Energy in Transport'
        ]
        for energy_type in energy_types:
            assert energy_type in expected_types, f"Unexpected energy type: {energy_type}"

    def test_load_data_country_codes(self):
        """Test that country codes are properly handled."""
        df = load_data()
        assert isinstance(df, pd.DataFrame)
        # Check that EL is converted to GR
        assert 'EL' not in df['Code'].values, "EL should be converted to GR"
        if 'GR' in df['Code'].values:
            greece_data = df[df['Code'] == 'GR']
            assert not greece_data.empty, "Greece data should exist"

    def test_load_data_numeric_columns(self):
        """Test that numeric columns are properly converted."""
        df = load_data()
        assert isinstance(df, pd.DataFrame)
        assert df['Year'].dtype in ['int64', 'float64'], "Year should be numeric"
        assert df['Renewable Percentage'].dtype in ['int64', 'float64'], "Renewable Percentage should be numeric"

    def test_load_data_flags_present(self):
        """Test that flags are properly generated."""
        df = load_data()
        assert isinstance(df, pd.DataFrame)
        assert 'Flag' in df.columns
        # Check that flags are strings and not null for most entries
        flag_series = df['Flag']
        assert flag_series.dtype == 'object'
        assert not flag_series.isnull().all()

class TestUtilityFunctions:
    """Test suite for utility functions."""
    
    @pytest.mark.parametrize("iso2,flag", [
        ("DE", "🇩🇪"),
        ("FR", "🇫🇷"),
        ("SE", "🇸🇪"),
        ("GR", "🇬🇷"),
        ("IT", "🇮🇹"),
    ])
    def test_iso2_to_flag(self, iso2, flag):
        """Test ISO2 to flag conversion."""
        assert iso2_to_flag(iso2) == flag

    def test_iso2_to_flag_invalid(self):
        """Test flag conversion with invalid codes."""
        result = iso2_to_flag("XX")
        assert isinstance(result, str), "Should return a string even for invalid codes"

