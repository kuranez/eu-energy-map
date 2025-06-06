# components/widgets.py

import panel as pn

def create_widgets(df_renewable):
    year_slider = pn.widgets.IntSlider(
        name='Year', start=2004, end=2022, step=1, value=2022
    )

    country_select = pn.widgets.Select(
        name='Country', options=sorted(df_renewable['Country'].unique().tolist()), value='Germany'
    )

    return year_slider, country_select