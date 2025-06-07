# layout/dashboard.py

import panel as pn
from panel.pane import Plotly


def build_layout(interactive_map, interactive_bar_year, interactive_bar_country, year_slider, country_select):
    """
    Baut das gesamte Panel-Layout zusammen

    Parameters:
    - interactive_map: Karte (Plotly Map)
    - interactive_bar_year: Balkendiagramm für Jahr
    - interactive_bar_country: Zeitreihe für Land
    - year_slider: IntSlider Widget
    - country_select: Select Widget

    Returns:
    - FastListTemplate Dashboard zur Anzeige
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
        sidebar=[],
        main=[layout]
    )

    return template