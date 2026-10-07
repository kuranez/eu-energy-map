# config.py

# Imports
import panel as pn
from pathlib import Path

# Panel extension setup
pn.extension('tabulator', 'plotly', design='material')

# Base directory of the project
BASE_DIR = Path(__file__).parent

# Assets directory
ASSETS_DIR = BASE_DIR / "assets"

# Logo path
LOGO_PATH = ASSETS_DIR / "logo-500px.png"

# Picture path
PICTURE_PATH = ASSETS_DIR / "europe-renewables-500px.png"

# Mapbox token for Plotly maps (if needed)
MAPBOX_TOKEN = 'your_mapbox_token'

# Data Mappings
COLUMN_MAPPING = {
    'nrg_bal': 'Energy Type',
    'TIME_PERIOD': 'Year',
    'OBS_VALUE': 'Renewable Percentage',
    'NAME_ENGL': 'Country'
}

COLUMNS_TO_DROP = [
    'DATAFLOW',
    'LAST UPDATE',
    'freq',
    'unit',
    'OBS_FLAG',
    'CONF_STATUS',
    'geo',
    'geo_key'
]

ENERGY_TYPE_MAPPING = {
    'Renewable energy - overall': 'Renewable Energy Total',
    'Renewable energy - electricity': 'Renewable Electricity',
    'Renewable energy - heating and cooling': 'Renewable Heating and Cooling',
    'Renewable energy - transport': 'Renewable Energy in Transport',
    'REN': 'Renewable Energy Total',
    'R5110-5150_W6000RIS': 'Renewable Energy Total',
    'REN_ELC': 'Renewable Electricity',
    'REN_HEAT_CL': 'Renewable Heating and Cooling',
    'REN_TRA': 'Renewable Energy in Transport'
}

COUNTRY_CODE_MAPPING = {
    'EL': 'GR',
    'UK': 'GB'
}

EU_COUNTRIES = {
    "AT", "BE", "BG", "HR", "CY", "CZ", "DK", 
    "EE", "FI", "FR", "DE", "EL", "HU", "IE", 
    "IT", "LV", "LT", "LU", "MT", "NL", "PL", 
    "PT", "RO", "SK", "SI", "ES", "SE"
}

NORMALIZE_ENERGY_MAPPING = {
    'REN': 'Renewable energy - overall',
    'R5110-5150_W6000RIS': 'Renewable energy - overall',
    'Renewable energy - overall': 'Renewable energy - overall',
}

FINAL_COLUMNS = [
    'Code', 'Flag', 'Country', 'Energy Type', 'Renewable Percentage', 'Year',
    'CNTR_ID', 'ISO2_Code', 'ISO3_CODE', 'geometry'
]