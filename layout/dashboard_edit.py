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
    layout = pn.Column(
        Plotly(interactive_map),
        tabs,
        sizing_mode="stretch_width"
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