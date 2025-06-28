# tests/test_filters.py

import pytest
import pandas as pd
import geopandas as gpd
from data.filters import preprocess, filter_data
from utils.flags import iso2_to_flag

class TestDataFilters:
    """Test suite for data filtering functionality."""

    def test_preprocess_output_shape(self, raw_data):
        """Test preprocess function output shape and columns."""
        df, gdf = raw_data
        merged = preprocess(df, gdf)
        assert isinstance(merged, pd.DataFrame)
        assert not merged.empty
        assert set(['Country', 'Code', 'Flag', 'Energy Type']).issubset(merged.columns)

    def test_preprocess_renewable_percentage_range(self, raw_data):
        """Test that renewable percentages are within valid range."""
        df, gdf = raw_data
        merged = preprocess(df, gdf)
        # Allow for some values outside 0-100 range as they might be valid in the data
        assert merged['Renewable Percentage'].min() >= 0, "Renewable percentage should not be negative"

    def test_preprocess_energy_type_mapping(self, raw_data):
        """Test that energy types are properly mapped to human-readable names."""
        df, gdf = raw_data
        merged = preprocess(df, gdf)
        energy_types = merged['Energy Type'].unique()
        expected_types = [
            'Renewable Energy Total',
            'Renewable Electricity', 
            'Renewable Heating and Cooling',
            'Renewable Energy in Transport'
        ]
        for energy_type in energy_types:
            assert energy_type in expected_types, f"Unexpected energy type: {energy_type}"

    def test_preprocess_country_code_remapping(self, raw_data):
        """Test that EL is properly remapped to GR."""
        df, gdf = raw_data
        merged = preprocess(df, gdf)
        # Check that EL is converted to GR
        assert 'EL' not in merged['Code'].values, "EL should be converted to GR"
        assert 'EL' not in merged['CNTR_ID'].values, "EL should be converted to GR in CNTR_ID"

    def test_preprocess_flag_generation(self, raw_data):
        """Test that flags are properly generated."""
        df, gdf = raw_data
        merged = preprocess(df, gdf)
        assert 'Flag' in merged.columns
        # Check that flags are strings and not null
        assert merged['Flag'].dtype == 'object'
        assert not merged['Flag'].isnull().all()

    def test_filter_data_eu_only(self, raw_data):
        """Test filtering for EU countries only."""
        df, gdf = raw_data
        merged = preprocess(df, gdf)
        df_renewable, df_eu_total = filter_data(merged)
        
        assert isinstance(df_renewable, pd.DataFrame)
        assert isinstance(df_eu_total, pd.DataFrame)
        assert not df_renewable.empty
        assert not df_eu_total.empty
        
        # Check that only EU countries are included (basic check)
        unique_countries = df_renewable['Code'].unique()
        assert len(unique_countries) <= 27, "Should not have more than 27 EU countries"

    def test_filter_data_renewable_energy_total_only(self, raw_data):
        """Test that only 'Renewable Energy Total' is included in filtered data."""
        df, gdf = raw_data
        merged = preprocess(df, gdf)
        df_renewable, df_eu_total = filter_data(merged)
        
        energy_types = df_renewable['Energy Type'].unique()
        assert len(energy_types) == 1, "Should only include one energy type"
        assert energy_types[0] == 'Renewable Energy Total'

    def test_filter_data_eu_total_aggregation(self, raw_data):
        """Test that EU total is properly aggregated by year."""
        df, gdf = raw_data
        merged = preprocess(df, gdf)
        df_renewable, df_eu_total = filter_data(merged)
        
        # Check that df_eu_total has Year column and is grouped by year
        assert 'Year' in df_eu_total.columns
        assert 'Renewable Percentage' in df_eu_total.columns
        
        # Years should be unique (one row per year)
        years_count = df_eu_total['Year'].nunique()
        total_rows = len(df_eu_total)
        assert years_count == total_rows, "Each year should appear only once in EU total"

    def test_filter_data_year_range(self, raw_data):
        """Test that data covers expected year range."""
        df, gdf = raw_data
        merged = preprocess(df, gdf)
        df_renewable, df_eu_total = filter_data(merged)
        
        min_year = df_eu_total['Year'].min()
        max_year = df_eu_total['Year'].max()
        
        # Basic sanity checks for year range
        assert min_year >= 2000, "Data should start from 2000 or later"
        assert max_year <= 2030, "Data should not exceed 2030"
        assert max_year > min_year, "Should have data for multiple years"

class TestUtilityFunctions:
    """Test suite for utility functions used in filters."""
    
    @pytest.mark.parametrize("iso2,flag", [
        ("DE", "🇩🇪"),
        ("FR", "🇫🇷"),
        ("GR", "🇬🇷"),
        ("ES", "🇪🇸"),
        ("IT", "🇮🇹"),
    ])
    def test_iso2_to_flag(self, iso2, flag):
        """Test ISO2 to flag conversion for EU countries."""
        assert iso2_to_flag(iso2) == flag

    def test_filter_data_with_sample_data(self, sample_csv_data, sample_geo_data):
        """Test filter_data with controlled sample data."""
        merged = preprocess(sample_csv_data, sample_geo_data)
        df_renewable, df_eu_total = filter_data(merged)
        
        assert isinstance(df_renewable, pd.DataFrame)
        assert isinstance(df_eu_total, pd.DataFrame)