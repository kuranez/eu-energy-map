from config import MAPBOX_TOKEN
from data.loader import load_energy_data
from data.filters import preprocess, filter_eu_data
from components.charts import *
from components.widgets import get_widgets
from layout.dashboard import build_layout

data, europe = load_energy_data(...)
merged = preprocess(data, europe)
df_renewable, df_eu_total = filter_eu_data(merged)

year_slider, country_select = get_widgets(df_renewable)
...

template = build_layout(...)
template.servable()