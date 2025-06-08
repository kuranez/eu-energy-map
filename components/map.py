# components/map.py

# Import necessary libraries

# Plotly for visualization
import plotly.graph_objects as go
# JSON for loading geojson data
import json
# Mapbox token for accessing Mapbox styles
from config import MAPBOX_TOKEN
# Custom utility functions for color scale normalization
from utils.colors import get_colorscale

# Create choropleth map using Plotly

def create_choropleth_map(df_year):
    fig = go.Figure(go.Choroplethmapbox(
        # Load the GeoJSON file for Europe
        geojson=json.load(open('./geo/europe.geojson')),
        # Use the 'Code' column for locations
        locations=df_year['Code'],
        # Use the 'Renewable Percentage' column for color intensity
        z=df_year['Renewable Percentage'],
        # Use a custom color scale defined in utils/colors.py
        colorscale=get_colorscale(),
        zmin=0,                # <--- FIXED!
        zmax=100,              # Color scale range
        # Set marker properties
        marker_opacity=0.8, marker_line_width=0.5,
        # Specify the feature ID key for the GeoJSON
        featureidkey="properties.CNTR_ID"
    ))
    fig.update_layout(
        # Set the Mapbox access token
        mapbox_accesstoken=MAPBOX_TOKEN,
        # Use a predefined Mapbox style
        mapbox_style="carto-positron",
        # Set the initial zoom level and center of the map
        mapbox_zoom=2.9,
        # Center the map on Europe
        mapbox_center={"lat": 54, "lon": 15},
        # Remove margins around the map
        margin={"r": 0, "t": 0, "l": 0, "b": 0}
    )
    return fig