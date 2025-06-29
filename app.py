# app.py

# Import necessary libraries
import panel as pn
import pandas as pd
import geopandas as gpd

# Import data loading and preprocessing functions
from data.loader import load_data
from data.filters import preprocess, filter_data

# Import components for the dashboard
from components.widgets import create_widgets
from components.map import create_choropleth_map
from components.charts.bar_chart_by_year import create_bar_chart_year 
from components.charts.bar_chart_by_country import create_bar_chart_country

# Import the layout builder
from layout.dashboard import build_layout

# Initialize Panel extension with required components
pn.extension('tabulator', 'plotly', design='material', sizing_mode='stretch_width')

# Load and preprocess data
data, europe = load_data(data_path='./data/nrg_ind_ren_linear.csv', geo_path='./geo/europe.geojson', return_raw=True)
# If preprocess expects a DataFrame, convert GeoDataFrame to DataFrame
merged = preprocess(data, europe)
if not isinstance(data, pd.DataFrame) or not isinstance(europe, gpd.GeoDataFrame):
    raise ValueError("load_data did not return expected DataFrame and GeoDataFrame")
df_renewable, df_eu_total = filter_data(merged)

# Widgets
year_slider, country_select = create_widgets(df_renewable)

# Bindings / interactive components
@pn.depends(year_slider.param.value)
def map_view(year):
    df_year = df_renewable[df_renewable['Year'] == year]
    return create_choropleth_map(df_year)

@pn.depends(year_slider.param.value)
def bar_by_year(year):
    df_year = df_renewable[df_renewable['Year'] == year]
    return create_bar_chart_year(df_year, year)

@pn.depends(country_select.param.value)
def bar_by_country(country):
    df_country = df_renewable[df_renewable['Country'] == country]
    return create_bar_chart_country(df_eu_total, df_country, country)

# Create the layout
template = build_layout(
    interactive_map=map_view,
    interactive_bar_year=bar_by_year,
    interactive_bar_country=bar_by_country,
    year_slider=year_slider,
    country_select=country_select
)

# Serve the application
template.servable()