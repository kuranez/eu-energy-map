# layout/dashboard.py

import panel as pn
from panel.pane import Plotly
from config import LOGO_PATH


def build_layout(interactive_map, interactive_bar_year, interactive_bar_country, year_slider, country_select):
    """
    Builds the complete Panel layout

    Parameters:
    - interactive_map: Map (Plotly Map)
    - interactive_bar_year: Bar chart for year
    - interactive_bar_country: Time series for country
    - year_slider: IntSlider widget
    - country_select: Select widget

    Returns:
    - FastListTemplate dashboard for display
    """
    # Ensure the layout is initialized
    pn.extension()
    # Markdown pane for description
    description = pn.pane.Markdown(
        """
        ## Renewable Energy Map of the European Union
        Explore renewable energy developments across Europe.

        ### Description
        This dashboard visualizes renewable energy data trends in the European Union, allowing users to filter by year and country.
        Use the tabs to explore different aspects of the data.
        
        Data is sourced from [Eurostat](https://ec.europa.eu/eurostat/databrowser/explore/all/envir?lang=en&subtheme=nrg&display=list&sort=category).

        ### Project Page on GitHub
        [https://github.com/kuranez/EU-Energy-Map](https://github.com/kuranez/EU-Energy-Map) \
        """,
        sizing_mode="stretch_width"
    )
    # Tab structure
    tabs = pn.Tabs(
        (
            'Year Filter',
            pn.Column(
                year_slider,
                Plotly(interactive_bar_year)
            )
        ),
        (
            'Country Filter',
            pn.Column(
                country_select,
                Plotly(interactive_bar_country)
            )
        )
    )

    # Main Layout
    layout = pn.Row(
        # Plotly panel
        Plotly(
            # Plotly map pane
            interactive_map, 
            # Margins (top, right, bottom, left)
             margin=(10, 10, 25, 10),
            # Stretch vertically
             sizing_mode="stretch_height",
             ),
        # Info panel
        pn.Column(
            # Description pane
            description,
            # Tabs for filters and charts
            tabs,
            sizing_mode="stretch_both",
            ),
    )

    # Template for the dashboard
    template = pn.template.FastListTemplate(
        title="EU Energy Map",
        logo=str(LOGO_PATH),
        theme="default",
        theme_toggle=False,
        sidebar=[],
        main=[layout]
    )

    return template