# EU Energy Map Notebook Release v1.1

## Overview
This release provides a fully interactive Jupyter Notebook version of the EU Energy Map project. It is designed for data exploration, prototyping, and documentation, allowing users to load, process, visualize, and analyze Eurostat renewable energy data directly within a notebook environment.

## What's Included
- **Notebook:** `eu-energy-map-nb.ipynb` with all code, workflow, and dashboard logic
- **Data:**
  - `./data/nrg_ind_ren_linear.csv` (Eurostat renewable energy data)
  - `./geo/europe.geojson` (GeoJSON boundaries for Europe)
- **Documentation:**
  - [notebook/documentation.md](notebook/documentation.md) — Function and workflow explanations
  - [notebook/changelog.md](notebook/changelog.md) — Notebook-specific changelog
- **README:** Usage, requirements, and project info

## Features
- Load, process, and explore Eurostat renewable energy data interactively
- View and analyze data tables, charts, and maps within the notebook
- Build and customize a dashboard with an interactive choropleth map and bar charts
- All logic and visualization steps are documented and reproducible in notebook cells
- Interactive widgets for filtering by year and country
- Consistent flag and country code handling (EL/GR)

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

## License
This project is licensed under the MIT License.

## Project Page
- [GitHub: kuranez/EU-Energy-Map](https://github.com/kuranez/EU-Energy-Map)

---
For production dashboards and web apps, see the main Python application branch.
