# Documentation: EU Energy Map

## 📌 Summary

An interactive dashboard that visualizes Eurostat data on renewable energy developments across European countries. Built with Python and Panel, the web app provides an intuitive interface to explore renewable energy trends from 2004 to 2024.

## 📦 Python Dependencies

- **Core:** `os`, `json`
- **Data Handling:** `pandas`, `geopandas`
- **Visualization:** `plotly.express`, `plotly.graph_objects`, `plotly.io`
- **Dashboard UI:** `panel`

## 📊 Datasets

### 1. Renewable Energy Data (Eurostat) - 2004–2022

- **File:** `nrg_ind_ren_linear_old.csv`
- **Source:** [Eurostat – Renewable Energy](https://ec.europa.eu/eurostat/databrowser/view/nrg_ind_ren/default/table?lang=en)
- **Years:** 2004–2022
- **Columns:** Country codes, energy type, unit, value (%), flags
- **Categories:** Total renewables, electricity, heating/cooling, transport

### 2. Renewable Energy Data (Eurostat) - 2015–2024

- **File:** `nrg_ind_ren_linear.csv`
- **Source:** [Eurostat – Renewable Energy](https://ec.europa.eu/eurostat/databrowser/view/nrg_ind_ren/default/table?lang=en)
- **Years:** 2015–2024
- **Columns:** Country names, energy type, unit, value (%), flags, confidentiality status
- **Categories:** Total renewables

### 3. Geographic Boundaries (GISCO - Eurostat)

- **File:** `europe.geojson`
- **Source:** [GISCO – Eurostat](https://ec.europa.eu/eurostat/web/gisco/geodata/administrative-units/countries)
- **Year:** 2024
- **Format:** GeoJSON (EPSG:4326), scale 1:20M

## 📁 Contents

```txt
eu-energy-map/
|
├── app.py                            # Main dashboard entry point
├── config.py                         # Configurations (tokens, paths, etc)
|
├── docs/
│   ├── documentation.md              # Project Documentation
│   └── notebook.ipynb                # Interactive Notebook
|
├── data/
│   ├── loader.py                     # Loads and merges CSV/GeoJSON data
│   ├── filters.py                    # Preprocessing and filtering logic
│   ├── nrg_ind_ren_linear_old.csv    # Eurostat renewable energy data
│   └── nrg_ind_ren_linear.csv        
|
├── components/
│   ├── charts/
│   │   ├── bar_chart_by_country.py   # Bar chart: Country vsU
│   │   └── bar_chart_by_year.py      # Bar chart: All countries by year
│   ├── map.py                        # Interactive choropleth map
│   └── widgets.py                    # Dashboard widgets (sliders, selectors)
|
├── layout/
│   └── dashboard.py                  # Layout composition for Panel
|
├── utils/                            # Helper functions
│   ├── colors.py                     # Color scales & conversion
│   └── flags.py                      # ISO2 code → emoji flag
|
├── assets/
│   ├── europe-renewables-500px.png   # Dashboard image
│   └── logo-500px.png               # Logo
|
└── geo/
    └── europe.geojson                # European country boundaries (GeoJSON)
```

## 📖 Documentation

### 1. Main dashboard entry point: `main.py`

### 2. Configuration: `config.py`

### 3. Data Loading & Filtering Pipeline: `data/`

### 4. Dashboard Components: `components/`

### 5. Dashboard Layout: `layout/`

### 6. Utilities: `utils/`

### 7. Assets: `assets/`

### 8. Geodata: `geo/`
