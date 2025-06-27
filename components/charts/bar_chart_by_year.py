# components/charts/bar_chart_by_year.py

import plotly.graph_objects as go
from utils.colors import get_viridis_color, get_colorscale

# Create bar chart for renewable energy by year
def create_bar_chart_year(df_year, year):
    """    
    Returns a bar chart showing the share of renewable energy in the EU for a specific year.
    
    Args:
        df_year (DataFrame): DataFrame containing renewable energy data for the specified year.
        year (int): The year for which the bar chart is created.
    
    Returns:
        fig (Figure): A Plotly Figure object containing the bar chart.
    """
    
    # Prepare the data for the bar chart

    # Sort the DataFrame by Renewable Percentage
    df_year = df_year.sort_values(by='Renewable Percentage')
    # Calculate the average renewable percentage for the EU
    eu_total_avg = df_year['Renewable Percentage'].mean()
    # Get a color for the EU average using a utility function
    scaled_color = get_viridis_color(eu_total_avg, fmt='hex')


    # Create a bar trace for renewable energy percentages by country
    # This trace will display the renewable energy percentage for each country 

    bar_trace = go.Bar(
        # Country names on x-axis, Renewable Percentage on y-axis
        x=df_year['Country'],
        y=df_year['Renewable Percentage'],
        # Use a color scale for the bars
        marker=dict(
            color=df_year['Renewable Percentage'], 
            coloraxis='coloraxis'),

        # Custom hover template for each bar
        hovertemplate="Renewable Share: <b>%{y:.1f}%</b><br>" +
                      "Country: <b>%{customdata[0]}</b> %{customdata[1]}",

        # Pass country name and flag as customdata for hovertemplate
        customdata=df_year[['Country', 'Flag']].values,
        
        # Set trace name to selected year
        name=f"<b>{year}</b>",

        # Hide legend
        showlegend=False
    )
   
    # Create a line for the EU average
    # This line will represent the average renewable energy percentage for the EU 

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
            width=4),
        # Custom hover template for the EU average
        hovertemplate="Renewable Share: <b>%{y:.1f}%</b>",
        # Fix to suppress showing trace info in the legend
        name="<b>EU Total Average</b> 🇪🇺",
        # Show legend for the EU average line
        showlegend=True
    )

    # Create the figure with the bar trace and the two scatter traces
    # This will combine the bar chart and the average lines into one figure 
    
    fig = go.Figure([bar_trace, scatter_avg])

    
    # Update the layout of the figure
    # This will set the title, axis labels, color scale, and other layout properties 

    fig.update_layout(
        # Set the title of the chart
        title=f"<b>Share of Renewable Energy in the European Union in {year}</b>",
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

        # Legend properties
        legend=dict(
            orientation="h", 
            yanchor="top", y=0.97, 
            xanchor="left", x=0.01),
        
        # Set the height of the chart
        height=400,
    )
    return fig