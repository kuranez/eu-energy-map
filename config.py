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
