# layout/dashboard.py

import panel as pn
from panel.pane import Plotly
from config import LOGO_PATH, PICTURE_PATH


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
    # Markdown pane: title and short description
    title_md = pn.pane.Markdown(
        """
        # 🌱 Renewable Energy in the European Union: Explore developments across Europe
        """,
    )
    # Markdown pane: information about the dashboard
    description_md = pn.pane.Markdown(
        """
        <style>
        .custom-desc { font-size: 16px; }
        .custom-desc h3 { font-size: 1.05em; }
        </style>
        <div class="custom-desc">

        ### 📑 Description
        This dashboard visualizes renewable energy data trends in the European Union, 
        allowing users to filter by year and country. Data is sourced from 
        [Eurostat](https://ec.europa.eu/eurostat/databrowser/view/nrg_ind_ren/default/table?lang=en&category=nrg.nrg_quant.nrg_quanta.nrg_ind_share).
        
        ### ❓ How to Use
        Use the tabs to explore different aspects of the data.

        ### 🌐 Project Page on GitHub
        [https://github.com/kuranez/EU-Energy-Map](https://github.com/kuranez/EU-Energy-Map) \
        """,
    )
    # Picture pane for the description
    description_png = pn.pane.PNG(
        str(PICTURE_PATH),
        width=250, height=250,
    
    )
    # Full description - Combines the markdown and picture panes
    description = pn.Row(
        description_md,
        description_png,
    )
    # Tab structure for filters and charts
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
            margin=(0, 20, 20, 0),
            # Stretch vertically
             sizing_mode="stretch_height",
             ),
        # Info panel
        pn.Column(
            # Title pane
            title_md,
            # Tabs for filters and charts
            tabs,
            # Description pane
            description,
            margin=(0, 0, 0, 0),
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