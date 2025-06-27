# components/widgets.py

import panel as pn

def create_widgets(df_renewable):
    """
    Create widgets for year selection and country selection.

    These widgets will be used to filter the data in the dashboard
    and update the visualizations accordingly.

    Args:
        df_renewable (pd.DataFrame): DataFrame containing renewable energy data.

    Returns:
        tuple: (year_slider, country_select) Panel widgets.
    """
    year_slider = pn.widgets.IntSlider(
        name='Year', start=2004, end=2022, step=1, value=2022
    )

    country_select = pn.widgets.Select(
        name='Country', options=sorted(df_renewable['Country'].unique().tolist()), value='Germany'
    )

    return year_slider, country_select

