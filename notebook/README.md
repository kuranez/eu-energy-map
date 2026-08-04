# EU Energy Map Notebook

This release is dedicated to working with the EU Energy Map project directly in Jupyter Notebook.

## Features
- Load, process, and explore Eurostat renewable energy data interactively
- View and analyze data tables, charts, and maps within the notebook
- Build and customize a dashboard with an interactive choropleth map and bar charts
- All logic and visualization steps are documented and reproducible in notebook cells

## Usage
1. Open `eu-energy-map-nb.ipynb` in Jupyter Notebook or JupyterLab.
2. Run cells step by step to load data, process it, and visualize results.
3. Use the interactive widgets to filter by year or country and explore the dashboard.

## Requirements
- Python 3.8+
- Jupyter Notebook or JupyterLab
- Required packages: `pandas`, `geopandas`, `panel`, `plotly`

Install dependencies with:
```bash
pip install pandas geopandas panel plotly
```

## Data
- Renewable energy data: `../data/nrg_ind_ren_linear.csv`
- GeoJSON boundaries: `../geo/europe.geojson`

## Project Page
- [GitHub: kuranez/EU-Energy-Map](https://github.com/kuranez/EU-Energy-Map)

---
This notebook release is for data exploration, prototyping, and documentation. For production dashboards and web apps, see the main Python application branch.
