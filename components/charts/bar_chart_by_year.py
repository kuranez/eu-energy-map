# components/charts/bar_chart_by_year.py

import plotly.graph_objects as go
from utils.colors import get_viridis_color, get_colorscale

# Create bar chart for renewable energy by year
def create_bar_chart_year(df_year, year):
    """ Prepare the data for the bar chart"""
    # Sort the DataFrame by Renewable Percentage
    df_year = df_year.sort_values(by='Renewable Percentage')
    # Calculate the average renewable percentage for the EU
    eu_total_avg = df_year['Renewable Percentage'].mean()
    # Get a color for the EU average using a utility function
    scaled_color = get_viridis_color(eu_total_avg, fmt='hex')

    """ 
    Create a bar trace for renewable energy percentages by country
        - This trace will display the renewable energy percentage for each country 
    """
    bar_trace = go.Bar(
        # Country names on x-axis, Renewable Percentage on y-axis
        x=df_year['Country'],
        y=df_year['Renewable Percentage'],
        # Use a color scale for the bars
        marker=dict(
            color=df_year['Renewable Percentage'], 
            coloraxis='coloraxis'),
        # Custom hover template for each bar
        hovertemplate="Country: %{customdata[0]}<b>%{customdata[1]}</b><br>Renewable: <b>%{y:.1f}%</b>",
        # Custom data for hover info
        customdata=df_year[['Flag', 'Country']].values,
        # Hide legend
        showlegend=False
    )

    """     
    Create a border line for the EU average
        - This line will be used to visually separate the EU average from the bars
    """
    scatter_border = go.Scatter(
        # Year on x-axis, EU average on y-axis
        x=df_year['Country'],
        y=[eu_total_avg] * len(df_year),
        # Use lines for the border
        mode="lines",
        # Solid line with a specific color
        line=dict(
            dash="solid", 
            color="rgba(255,255,255,0.7)", 
            width=4),
        # Skip hover info for the border line
        hoverinfo="skip",
        # Hide legend for the border line
        showlegend=False
    )

    """     
    Create a line for the EU average
        - This line will represent the average renewable energy percentage for the EU 
    """
    scatter_avg = go.Scatter(
        # Year on x-axis, EU average on y-axis
        x=df_year['Country'],
        y=[eu_total_avg] * len(df_year),
        # Use lines for the average
        mode="lines",
        # Solid line with the scaled color
        line=dict(
            dash="solid", 
            color=scaled_color, 
            width=2),
        # Custom hover template for the EU average
        hovertemplate="🇪🇺 EU Avg: <b>%{y:.1f}%</b>",
        # Hide legend for the EU average line
        showlegend=False
    )

    """
    Create the figure with the bar trace and the two scatter traces
        - This will combine the bar chart and the average lines into one figure 
    """
    fig = go.Figure([bar_trace, scatter_border, scatter_avg])

    """
    Update the layout of the figure
        - This will set the title, axis labels, color scale, and other layout properties 
    """
    fig.update_layout(
        # Set the title of the chart
        title=f"Renewable Energy by Country in {year}",
        # Set x-axis title to None (no title)
        xaxis_title=None,
        # Set y-axis title
        yaxis_title="Renewable Energy (%)",
        # Set the color axis properties
        coloraxis=dict(
            colorscale=get_colorscale(),
            cmin=0, cmax=100,
            colorbar=dict(
                tickvals=[0, 20, 40, 60, 80, 100], 
                ticktext=["0%", "20%", "40%", "60%", "80%", "100%"])
        ),
        # Set margins around the chart
        margin={"t": 50, "b": 50, "l": 50, "r": 50},
        # Set the height of the chart
        height=450
    )
    return fig