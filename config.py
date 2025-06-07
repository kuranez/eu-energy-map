# config.py

# Imports
import panel as pn
from pathlib import Path

# Panel extension setup
pn.extension('tabulator', 'plotly', design='material', sizing_mode='stretch_width')

# Mapbox token for Plotly maps
MAPBOX_TOKEN = 'your_mapbox_token'

# Base directory of the project
BASE_DIR = Path(__file__).parent

# Assets directory
ASSETS_DIR = BASE_DIR / "assets"

# Logo path
LOGO_PATH = ASSETS_DIR / "logo.svg"
