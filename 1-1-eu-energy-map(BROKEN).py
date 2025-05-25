# EU-Energy-Map
# Version 1.1
# Author: github.com/kuranez

############################################################################################################

### I. Import

import os
import json

import panel as pn
import pandas as pd
import geopandas as gpd
import plotly.express as px
import plotly.graph_objects as go
import plotly.io as pio
from plotly.colors import sample_colorscale

############################################################################################################

### II. Settings

# Initialize Panel extension
pn.extension('tabulator', 'plotly', design='material', sizing_mode='stretch_width')

# Set MapBox access token
MAPBOX_TOKEN = 'pk.eyJ1Ijoia3VyYW5leiIsImEiOiJjbTJmMjI0d2kwNDVxMnFzYXNldnc1N2VsIn0.t11TYpF2QBdid-hQfW8mig'

############################################################################################################

### III. Methods

def load_data():
    """Load energy data and European geojson data."""
    data = pd.read_csv('./data/nrg_ind_ren_linear.csv')
    europe_gdf = gpd.read_file("./geo/europe.geojson")

    merged_data = europe_gdf.merge(data, left_on='CNTR_ID', right_on='geo')

    merged_data.rename(columns={
        'nrg_bal': 'Energy Type', 'TIME_PERIOD': 'Year',
        'OBS_VALUE': 'Renewable Percentage', 'geo': 'Code',
        'NAME_ENGL': 'Country'
    }, inplace=True)

    energy_type_map = {
        'REN': 'Renewable Energy Total',
        'REN_ELC': 'Renewable Electricity',
        'REN_HEAT_CL': 'Renewable Heating and Cooling',
        'REN_TRA': 'Renewable Energy in Transport'
    }
    merged_data['Energy Type'] = merged_data['Energy Type'].replace(energy_type_map)

    merged_data.drop(columns=['LAST UPDATE', 'freq', 'unit', 'OBS_FLAG'], inplace=True)
    merged_data[['Year', 'Renewable Percentage']] = merged_data[['Year', 'Renewable Percentage']].apply(pd.to_numeric)
    merged_data['Renewable Percentage'] = merged_data['Renewable Percentage'].round(1)
    merged_data['Flag'] = merged_data['Code'].apply(iso2_to_flag)

    final_columns = [
        'Code', 'Flag', 'Country', 'Energy Type', 'Renewable Percentage', 'Year',
        'CNTR_ID', 'ISO3_CODE', 'geometry'
    ]
    return merged_data[final_columns]

@pn.cache
def iso2_to_flag(iso2_code):
    """Convert ISO2 country code to flag emoji."""
    return chr(0x1F1E6 + ord(iso2_code[0]) - ord('A')) + chr(0x1F1E6 + ord(iso2_code[1]) - ord('A'))

def filter_data(merged_data):
    """Filter and structure dataset for visualization."""
    eu_countries = {"AT", "BE", "BG", "HR", "CY", "CZ", "DK", "EE", "FI", "FR", "DE", "GR", "HU", "IE", "IT", "LV", "LT",
                    "LU", "MT", "NL", "PL", "PT", "RO", "SK", "SI", "ES", "SE"}
    df_renewable = merged_data[(merged_data['Energy Type'] == 'Renewable Energy Total') & merged_data['Code'].isin(eu_countries)]
    df_eu_total = df_renewable.groupby('Year', as_index=False)['Renewable Percentage'].mean()
    return df_renewable, df_eu_total

@pn.cache
def create_choropleth_map(df_year):
    """Generate a Choropleth map of renewable energy percentages."""
    fig = go.Figure(go.Choroplethmapbox(
        geojson=json.load(open('./geo/europe.geojson')),
        locations=df_year['Code'],
        z=df_year['Renewable Percentage'],
        colorscale="Viridis",
        marker_opacity=0.8, marker_line_width=0.5,
        featureidkey="properties.CNTR_ID"
    ))
    fig.update_layout(mapbox_accesstoken=MAPBOX_TOKEN, mapbox_style="carto-positron", mapbox_zoom=3,
                      mapbox_center={"lat": 54, "lon": 15}, margin={"r": 0, "t": 0, "l": 0, "b": 0})
    return fig


# Create bar chart by year for all countries
@pn.cache
def create_bar_chart_year(df_year, year):
    # Sort dataframe by renewable percentage in ascending order
    df_year = df_year.sort_values(by='Renewable Percentage')

    # Calculate EU total average renewable percentage for 2022
    eu_total_avg = df_year['Renewable Percentage'].mean()

    # Map EU total average to a color in the Viridis scale
    color_scale = px.colors.sequential.Viridis
    normalized_avg = eu_total_avg / 100  # Normalize average to a 0-1 range
    scaled_color = sample_colorscale(color_scale, normalized_avg)[0]
    
    # Create bar trace (main layer)
    bar_trace = go.Bar(
        x=df_year['Country'],
        y=df_year['Renewable Percentage'],
        marker=dict(
            color=df_year['Renewable Percentage'],
            coloraxis='coloraxis',  # Link to coloraxis
        ),
        name="",  # Fix to hide trace info
        hovertemplate="Country: %{customdata[0]}"
                      "<b>%{customdata[1]}</b><br>"
                      "Renewable Percentage: <b>%{y:.1f}%</b>",
        customdata=df_year[['Flag', 'Country']].values,  # Attach custom data
        showlegend=False,
    )
    
    # Add scatter trace for EU Total Average (border layer)
    scatter_trace_border = go.Scatter(
        x=df_year['Country'],  # Use all countries to make the line span across
        y=[eu_total_avg] * len(df_year),  # Duplicate average value for each country
        mode="lines",
        line=dict(dash="solid", color="rgba(255, 255, 255, 0.7)", width=4),
        hoverinfo="skip",  # Suppress hover for border layer
        showlegend=False,
    )
    
    # Add scatter trace for EU Total Average (main layer)
    scatter_trace = go.Scatter(
        x=df_year['Country'],  # Use all countries to make the line span across
        y=[eu_total_avg] * len(df_year),  # Duplicate average value for each country
        mode="lines",
        line=dict(dash="solid", color=scaled_color, width=2),
        hovertemplate="🇪🇺 EU Total Average:<b> %{y:.1f}%</b>",
        name="",  # Fix to suppress showing trace info
        showlegend=False,
    )

    # Create figure
    fig = go.Figure(data=[bar_trace, scatter_trace_border, scatter_trace])

    # Update layout
    fig.update_layout(
        title=f"Renewable Energy Percentage by Country in {year}",
        xaxis=dict(title=None),
        yaxis=dict(title="Renewable Energy (%)"),
        coloraxis=dict(  # Define coloraxis for color bar
            colorscale='Viridis',
            cmin=0,
            cmax=100,
            colorbar=dict(
                orientation="v",
                title=None,
                tickvals=[0, 20, 40, 60, 80, 100],
                ticktext=["0%", "20%", "40%", "60%", "80%", "100%"],
            ),
        ),
        margin={"t": 50, "b": 50, "l": 50, "r": 50},
        height=450,
    )

    return fig

# Create Country Chart
@pn.cache
def create_bar_chart_country(df_eu_total, df_country, country):
    # Calculate the average renewable energy percentage for all years (used for annotation)
    eu_total_avg = df_eu_total['Renewable Percentage'].mean()
    
    # Map EU total average to a color in the Viridis scale
    color_scale = px.colors.sequential.Viridis
    normalized_avg = eu_total_avg / 100  # Normalize average to a 0-1 range
    scaled_color = sample_colorscale(color_scale, normalized_avg)[0]

    # Create the figure with Plotly
    fig = go.Figure()

    # Add the line trace for EU total renewable energy percentage over the years
    fig.add_trace(go.Scatter(
        x=df_eu_total['Year'], 
        y=df_eu_total['Renewable Percentage'], 
        mode='lines+markers',
        line=dict(color=scaled_color, width=3),
        marker=dict(
            size=6,
            color=df_eu_total['Renewable Percentage'],  # Map the renewable percentage to color
            colorscale='Viridis',
            coloraxis="coloraxis",
        ),
        hovertemplate="🇪🇺 %{x}: <b>%{y:.1f}%</b>",
        name="EU Total",
    ))

    # Add the bar trace for the selected country's renewable energy percentage
    fig.add_trace(go.Bar(
        x=df_country['Year'], 
        y=df_country['Renewable Percentage'],
        marker=dict(
            color=df_country['Renewable Percentage'],  # Map the renewable percentage to color
            colorscale='Viridis',
            coloraxis="coloraxis",
        ),
        customdata=df_country[['Flag', 'Country']].values,  # Attach custom data
        hovertemplate="Country: %{customdata[0]} "
                      "<b>%{customdata[1]}</b><br>"
                      "Year: <b>%{x}</b><br>"
                      "Renewable Percentage: <b>%{y:.1f}%</b>",
        name="",
        showlegend=False,
    ))

    # Define the layout with legend at the bottom
    fig.update_layout(
        title=f"Renewable Energy Percentage ({country}, 2004-2022)",
        xaxis=dict(
            title="Year",
            showgrid=False,
            showline=True,
            tickmode="linear",
            tick0=2005,
            dtick=5,
            range=[2003.5, 2022.5],
        ),
        yaxis=dict(
            title="Renewable Energy (%)",
        ),
        coloraxis=dict(
            colorscale='Viridis',
            cmin=0,
            cmax=100,
            colorbar=dict(
                orientation="v",
                tickvals=[0, 20, 40, 60, 80, 100],
                ticktext=["0%", "20%", "40%", "60%", "80%", "100%"],
            ),
        ),
        height=450,
        margin={"t": 50, "b": 50, "l": 50, "r": 50},
        showlegend=True,
        legend=dict(
            orientation="h",
            yanchor="top",
            y=1-0.01,
            xanchor="left",
            x=0+0.01
        ),
    )

    return fig

############################################################################################################

### IV. Main

# Load and preprocess data
merged_data = load_data()
df_renewable, df_eu_total = filter_data(merged_data)
selected_year, selected_country = 2022, "Germany"
df_year = df_renewable[df_renewable['Year'] == selected_year]
df_country = df_renewable[df_renewable['Country'] == selected_country]

############################################################################################################

### V. Dashboard

# Widgets
year_slider = pn.widgets.IntSlider(name='Year', start=2004, end=2022, step=1, value=selected_year)
country_selection = pn.widgets.Select(name='Country', options=df_renewable['Country'].unique().tolist(), value=selected_country)

# Interactive components
interactive_map = pn.bind(create_choropleth_map, year_slider)
interactive_bar_chart_year = pn.bind(create_bar_chart_year, year=year_slider)
interactive_bar_chart_country = pn.bind(create_bar_chart_country, df_eu_total, country_selection.param.value)

# Layout
tabs = pn.Tabs(
    ('Year Filter', pn.Column(year_slider, pn.pane.Plotly(interactive_bar_chart_year))),
    ('Country Filter', pn.Column(country_selection, pn.pane.Plotly(interactive_bar_chart_country)))
)
layout = pn.Column(pn.pane.Plotly(interactive_map), tabs)

pn.template.FastListTemplate(title="EU Energy Map", sidebar=[], main=[layout]).servable()
