import panel as pn

def build_layout(map_plot, bar_by_year, bar_by_country, year_slider, country_select):
    tabs = pn.Tabs(...)
    layout = pn.Column(pn.pane.Plotly(map_plot), tabs)
    return pn.template.FastListTemplate(..., main=[layout])