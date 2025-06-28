# tests/test_helpers.py

import pytest
import pandas as pd
import geopandas as gpd
import os
from utils.helpers import (
    load_csv_data, load_gdf, load_geojson, 
    merge_data, rename_columns, load_and_combine_csv_data
)

class TestHelperFunctions:
    """Test suite for utility helper functions."""

    def test_load_csv_data_success(self):
        """Test successful CSV loading."""
        if os.path.exists('./data/nrg_ind_ren_linear.csv'):
            df = load_csv_data('./data/nrg_ind_ren_linear.csv')
            assert isinstance(df, pd.DataFrame)
            assert not df.empty
        else:
            pytest.skip("Test data file not found")

    def test_load_csv_data_file_not_found(self):
        """Test CSV loading with non-existent file."""
        result = load_csv_data('./nonexistent.csv')
        assert result is None

    def test_load_gdf_success(self):
        """Test successful GeoJSON loading as GeoDataFrame."""
        if os.path.exists('./geo/europe.geojson'):
            gdf = load_gdf('./geo/europe.geojson')
            assert isinstance(gdf, gpd.GeoDataFrame)
            assert not gdf.empty
            assert hasattr(gdf, 'geometry')
        else:
            pytest.skip("Test geo file not found")

    def test_load_gdf_file_not_found(self):
        """Test GeoDataFrame loading with non-existent file."""
        result = load_gdf('./nonexistent.geojson')
        assert result is None

    def test_load_geojson_success(self):
        """Test successful GeoJSON loading as dict."""
        if os.path.exists('./geo/europe.geojson'):
            geojson_data = load_geojson('./geo/europe.geojson')
            assert isinstance(geojson_data, dict)
            assert 'type' in geojson_data
        else:
            pytest.skip("Test geo file not found")

    def test_merge_data_success(self, sample_csv_data, sample_geo_data):
        """Test successful data merging."""
        merged = merge_data(sample_geo_data, sample_csv_data, 'CNTR_ID', 'geo')
        assert isinstance(merged, pd.DataFrame)
        assert not merged.empty
        # Check that columns from both dataframes are present
        assert 'CNTR_ID' in merged.columns
        assert 'geo' in merged.columns

    def test_merge_data_empty_result(self):
        """Test data merging with incompatible data."""
        df1 = pd.DataFrame({'A': [1, 2], 'B': [3, 4]})
        df2 = pd.DataFrame({'C': [5, 6], 'D': [7, 8]})
        
        # This should result in an empty merge
        result = merge_data(df1, df2, 'A', 'C')
        assert isinstance(result, pd.DataFrame)

    def test_rename_columns_default_mapping(self, sample_csv_data):
        """Test column renaming with default mapping."""
        renamed = rename_columns(sample_csv_data)
        expected_columns = ['Energy Type', 'Year', 'Renewable Percentage', 'Code', 'Country']
        
        # Check that at least some expected columns are present
        for col in ['Energy Type', 'Year', 'Renewable Percentage', 'Code']:
            if col in expected_columns:
                assert col in renamed.columns

    def test_rename_columns_custom_mapping(self, sample_csv_data):
        """Test column renaming with custom mapping."""
        custom_mapping = {'geo': 'Country_Code', 'nrg_bal': 'Energy_Type'}
        renamed = rename_columns(sample_csv_data, custom_mapping)
        
        assert 'Country_Code' in renamed.columns
        assert 'Energy_Type' in renamed.columns

class TestDataIntegration:
    """Test integration of helper functions with real data."""

    def test_full_loading_pipeline(self):
        """Test complete data loading pipeline using helpers."""
        # Skip if data files don't exist
        if not (os.path.exists('./data/nrg_ind_ren_linear.csv') and 
                os.path.exists('./geo/europe.geojson')):
            pytest.skip("Test data files not found")
        
        # Load data using helpers
        csv_data = load_csv_data('./data/nrg_ind_ren_linear.csv')
        geo_data = load_gdf('./geo/europe.geojson')
        
        assert csv_data is not None
        assert geo_data is not None
        
        # Merge data
        merged = merge_data(geo_data, csv_data, 'CNTR_ID', 'geo')
        assert not merged.empty
        
        # Rename columns
        renamed = rename_columns(merged)
        assert not renamed.empty

    def test_helper_functions_with_sample_data(self, sample_csv_data, sample_geo_data):
        """Test helper functions with controlled sample data."""
        # Test merging
        merged = merge_data(sample_geo_data, sample_csv_data, 'CNTR_ID', 'geo')
        assert isinstance(merged, pd.DataFrame)
        
        # Test renaming
        renamed = rename_columns(merged)
        assert isinstance(renamed, pd.DataFrame)
