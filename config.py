# config.py

# Imports
import panel as pn
from pathlib import Path

# Panel extension setup
pn.extension('tabulator', 'plotly', design='material')

# Mapbox token for Plotly maps
MAPBOX_TOKEN = 'your_mapbox_token'

# Base directory of the project
BASE_DIR = Path(__file__).parent

# Assets directory
ASSETS_DIR = BASE_DIR / "assets"

# Logo path
LOGO_PATH = ASSETS_DIR / "logo-500px.png"

# Picture path
PICTURE_PATH = ASSETS_DIR / "europe-renewables-500px.png"

# Energy type mappings from Eurostat codes to human-readable names
ENERGY_TYPE_MAPPING = {
    'REN': 'Renewable Energy Total',
    'REN_ELC': 'Renewable Electricity',
    'REN_HEAT_CL': 'Renewable Heating and Cooling',
    'REN_TRA': 'Renewable Energy in Transport'
}

# Country code mappings for data standardization
COUNTRY_CODE_MAPPING = {
    'EL': 'GR'  # Greece: EL (Eurostat) -> GR (ISO standard)
}

# EU member countries (as of 2025)
EU_COUNTRIES = {
    "AT", "BE", "BG", "HR", "CY", "CZ", "DK", "EE", "FI", "FR", 
    "DE", "GR", "HU", "IE", "IT", "LV", "LT", "LU", "MT", "NL", 
    "PL", "PT", "RO", "SK", "SI", "ES", "SE"
}

# Column mappings for data standardization
COLUMN_MAPPING = {
    'nrg_bal': 'Energy Type',
    'TIME_PERIOD': 'Year',
    'OBS_VALUE': 'Renewable Percentage',
    'geo': 'Code',
    'NAME_ENGL': 'Country'
}

# Columns to drop during data cleaning
COLUMNS_TO_DROP = ['LAST UPDATE', 'freq', 'unit', 'OBS_FLAG']