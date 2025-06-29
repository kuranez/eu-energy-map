# utils/helpers.py

"""
Legacy helper functions for EU Energy Map project.
This module now only contains data loading functions.
Other functions have been moved to:
- import_helpers.py: Mapping constants and data loading functions
- pd_helpers.py: Pandas data processing functions
"""

# Import data loading functions from import_helpers
from utils.import_helpers import (
    load_csv_data,
    load_and_combine_csv_data,
    load_geojson,
    load_gdf
)

# Re-export for backward compatibility
__all__ = [
    'load_csv_data',
    'load_and_combine_csv_data', 
    'load_geojson',
    'load_gdf'
]

