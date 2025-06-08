# components/charts.py

import plotly.express as px
import plotly.graph_objects as go
import json
import pandas as pd

from config import MAPBOX_TOKEN
from utils.colors import get_viridis_color, get_colorscale

# Create choropleth map using Plotly

def create_choropleth_map(df_year):
    fig = go.Figure(go.Choroplethmapbox(
        geojson=json.load(open('./geo/europe.geojson')),
        locations=df_year['Code'],
        z=df_year['Renewable Percentage'],
        colorscale=get_colorscale(),
        zmin=0,                # <--- FIXED!
        zmax=100,              # Color scale range
        marker_opacity=0.8, marker_line_width=0.5,
        featureidkey="properties.CNTR_ID"
    ))
    fig.update_layout(
        mapbox_accesstoken=MAPBOX_TOKEN,
        mapbox_style="carto-positron",
        mapbox_zoom=3,
        mapbox_center={"lat": 54, "lon": 15},
        margin={"r": 0, "t": 0, "l": 0, "b": 0}
    )
    return fig

# Create bar chart for renewable energy by year
def create_bar_chart_year(df_year, year):
    df_year = df_year.sort_values(by='Renewable Percentage')
    eu_total_avg = df_year['Renewable Percentage'].mean()
    scaled_color = get_viridis_color(eu_total_avg, fmt='hex')

    bar_trace = go.Bar(
        x=df_year['Country'],
        y=df_year['Renewable Percentage'],
        marker=dict(color=df_year['Renewable Percentage'], coloraxis='coloraxis'),
        hovertemplate="Country: %{customdata[0]}<b>%{customdata[1]}</b><br>Renewable: <b>%{y:.1f}%</b>",
        customdata=df_year[['Flag', 'Country']].values,
        showlegend=False
    )

    scatter_border = go.Scatter(
        x=df_year['Country'],
        y=[eu_total_avg] * len(df_year),
        mode="lines",
        line=dict(dash="solid", color="rgba(255,255,255,0.7)", width=4),
        hoverinfo="skip",
        showlegend=False
    )

    scatter_avg = go.Scatter(
        x=df_year['Country'],
        y=[eu_total_avg] * len(df_year),
        mode="lines",
        line=dict(dash="solid", color=scaled_color, width=2),
        hovertemplate="🇪🇺 EU Avg: <b>%{y:.1f}%</b>",
        showlegend=False
    )

    fig = go.Figure([bar_trace, scatter_border, scatter_avg])
    fig.update_layout(
        title=f"Renewable Energy by Country in {year}",
        xaxis_title=None,
        yaxis_title="Renewable Energy (%)",
        coloraxis=dict(
            colorscale=get_colorscale(),
            cmin=0, cmax=100,
            colorbar=dict(tickvals=[0, 20, 40, 60, 80, 100], ticktext=["0%", "20%", "40%", "60%", "80%", "100%"])
        ),
        margin={"t": 50, "b": 50, "l": 50, "r": 50},
        height=450
    )
    return fig

# Create bar chart for renewable energy by country
def create_bar_chart_country(df_eu_total, df_country, country):
    eu_total_avg = df_eu_total['Renewable Percentage'].mean()
    scaled_color = get_viridis_color(eu_total_avg, fmt='hex')

    fig = go.Figure()

    fig.add_trace(go.Scatter(
        x=df_eu_total['Year'],
        y=df_eu_total['Renewable Percentage'],
        mode='lines+markers',
        line=dict(color=scaled_color, width=3),
        marker=dict(size=6, color=df_eu_total['Renewable Percentage'], colorscale=get_colorscale(), coloraxis="coloraxis"),
        hovertemplate="🇪🇺 %{x}: <b>%{y:.1f}%</b>",
        name="EU Total",
    ))

    fig.add_trace(go.Bar(
        x=df_country['Year'],
        y=df_country['Renewable Percentage'],
        marker=dict(color=df_country['Renewable Percentage'], colorscale=get_colorscale(), coloraxis="coloraxis"),
        customdata=df_country[['Flag', 'Country']].values,
        hovertemplate="%{customdata[0]} %{customdata[1]}<br>%{x}: <b>%{y:.1f}%</b>",
        showlegend=False
    ))

    fig.update_layout(
        title=f"Renewable Energy Percentage ({country}, 2004-2022)",
        xaxis=dict(title="Year", tickmode="linear", tick0=2005, dtick=5, range=[2003.5, 2022.5]),
        yaxis_title="Renewable Energy (%)",
        coloraxis=dict(colorscale=get_colorscale(), cmin=0, cmax=100,
                       colorbar=dict(tickvals=[0, 20, 40, 60, 80, 100])),
        margin={"t": 50, "b": 50, "l": 50, "r": 50},
        showlegend=True,
        legend=dict(orientation="h", yanchor="top", y=0.99, xanchor="left", x=0.01)
    )
    return fig
