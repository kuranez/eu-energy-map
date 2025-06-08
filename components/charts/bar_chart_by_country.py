# components/charts/bar_chart_by_country.py

import plotly.graph_objects as go
from utils.colors import get_viridis_color, get_colorscale

# Create bar chart for renewable energy by country
def create_bar_chart_country(df_eu_total, df_country, country):
    """
    Returns a time‐series comparison of EU total vs. a single country.
    """
    # EU total average as a scatter‐line
    eu_avg = df_eu_total['Renewable Percentage'].mean()
    avg_color = get_viridis_color(eu_avg, fmt='hex')

    fig = go.Figure()

    # EU total as scatter‐line
    fig.add_trace(go.Scatter(
        # Year on x-axis, Renewable Percentage on y-axis
        x=df_eu_total['Year'],
        y=df_eu_total['Renewable Percentage'],
        
        # Use lines and markers for better visibility
        mode='lines+markers',

        # Use a solid line with a specific color
        line=dict(color=avg_color, width=3),
        
        # Add markers for each data point
        marker=dict(
            size=6, 
            color=df_eu_total['Renewable Percentage'], 
            colorscale=get_colorscale(), 
            coloraxis="coloraxis"),
        
        # Custom hover template for EU total
        hovertemplate="🇪🇺 %{x}: <b>%{y:.1f}%</b>",
        name="EU Total"
    ))

    # Single country as bars
    fig.add_trace(go.Bar(
        # Year on x-axis, Renewable Percentage on y-axis
        x=df_country['Year'],
        y=df_country['Renewable Percentage'],

        # Use a color scale for the bars
        marker=dict(
            color=df_country['Renewable Percentage'],
            colorscale=get_colorscale(), 
            coloraxis="coloraxis"),
        
        # Custom hover template for country
        customdata=df_country[['Flag', 'Country']].values,
        hovertemplate="%{customdata[0]} %{customdata[1]}<br>%{x}: <b>%{y:.1f}%</b>",
        
        # Hide legend for bars
        showlegend=False
    ))

    fig.update_layout(
        # Set the title of the chart
        title=f"Renewable Energy Percentage ({country}, 2004–2022)",
        # Set x-axis properties
        xaxis=dict(
            title="Year", 
            tickmode="linear", 
            dtick=5, 
            range=[2003.5, 2022.5]),
        # Set y-axis properties
        yaxis_title="Renewable Energy (%)",
        # Set color axis properties
        coloraxis=dict(
            colorscale=get_colorscale(), 
            cmin=0, cmax=100,
            colorbar=dict(tickvals=[0,20,40,60,80,100])
        ),
        # Set margins around the chart
        margin={"t":50,"b":50,"l":50,"r":50},
        # Legend properties
        legend=dict(
            orientation="h", 
            yanchor="top", y=0.99, 
            xanchor="left", x=0.01)
    )
    return fig
