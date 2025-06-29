# utils/mapping.py

"""
Data mapping utilities for EU Energy Map project.
This module is now a legacy wrapper around import_helpers.py
All constants and functions have been moved to import_helpers.py for better organization.
"""

# Import all mapping constants and functions from import_helpers
from utils.import_helpers import (
    ENERGY_TYPE_MAPPING,
    COUNTRY_CODE_MAPPING,
    EU_COUNTRIES,
    COLUMN_MAPPING,
    COLUMNS_TO_DROP,
    get_energy_type_mapping,
    get_country_code_mapping,
    get_eu_countries,
    get_column_mapping,
    get_columns_to_drop
)

# Re-export for backward compatibility
__all__ = [
    'ENERGY_TYPE_MAPPING',
    'COUNTRY_CODE_MAPPING',
    'EU_COUNTRIES',
    'COLUMN_MAPPING',
    'COLUMNS_TO_DROP',
    'get_energy_type_mapping',
    'get_country_code_mapping',
    'get_eu_countries',
    'get_column_mapping',
    'get_columns_to_drop'
]