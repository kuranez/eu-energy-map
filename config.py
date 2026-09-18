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

# Data
COLUMN_MAPPING = {}

COLUMNS_TO_DROP = []

ENERGY_TYPE_MAPPING = {
        'REN': 'Renewable Energy Total',
        'R5110-5150_W6000RIS': 'Renewable Energy Total',
        'REN_ELC': 'Renewable Electricity',
        'REN_HEAT_CL': 'Renewable Heating and Cooling',
        'REN_TRA': 'Renewable Energy in Transport'
}

COUNTRY_CODE_MAPPING = {
    'EL' : 'GR',
    'UK' : 'GB'
}

EU_COUNTRIES = {
    "AT", "BE", "BG", "HR", "CY", "CZ", "DK", 
    "EE", "FI", "FR", "DE", "EL", "HU", "IE", 
    "IT", "LV", "LT", "LU", "MT", "NL", "PL", 
    "PT", "RO", "SK", "SI", "ES", "SE"
}