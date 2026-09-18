# EU Energy Map

<p align="left">
    <a href="https://www.python.org/" target="_blank">
        <img src="https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white" alt="Python"/>
    </a>
    <a href="https://pandas.pydata.org/" target="_blank">
        <img src="https://img.shields.io/badge/Pandas-150458?style=for-the-badge&logo=pandas&logoColor=white" alt="Pandas"/>
    </a>
    <a href="https://geopandas.org/" target="_blank">
        <img src="https://img.shields.io/badge/Geopandas-008000?style=for-the-badge&logo=geopandas&logoColor=white" alt="Geopandas"/>
    </a>
    <a href="https://panel.holoviz.org/" target="_blank">
        <img src="https://img.shields.io/badge/Holoviz%20Panel-0094A9?style=for-the-badge" alt="Holoviz Panel"/>
    </a>
    <a href="https://jupyter.org/" target="_blank">
        <img src="https://img.shields.io/badge/Jupyter-F37626?style=for-the-badge&logo=jupyter&logoColor=white" alt="Jupyter"/>
    </a>
    <a href="https://docs.docker.com/" target="_blank">
        <img src="https://img.shields.io/badge/Docker-2496ED?style=for-the-badge&logo=docker&logoColor=white" alt="Docker"/>
    </a>
</p>

## Project Summary

The **EU Energy Map** transforms official Eurostat datasets into an interactive web dashboard for monitoring clean energy transitions across Europe (2004–2024).

- **Geospatial Mapping:** Interactive choropleth maps powered by Plotly (MapLibre) and Eurostat GeoJSON boundaries.
- **Comparative Benchmarking:** Real-time visual comparison of individual member states against EU27 aggregate averages.
- **Data Harmonization:** Automated ETL pipeline standardizing historical (2004–2022) and modern (2015–2024) Eurostat energy metrics.
- **Reactive UI:** Fast, reactive layout built with HoloViz Panel and Material Design components.

## 🌐 Web App

> [![Live Demo](https://img.shields.io/badge/🟢%20Live%20App-%20EU--Energy--Map-0057B7?style=for-the-badge)](https://apps.kuracodez.space/eu-energy-map/app)
>
> **Try the app - explore renewable energy data for Europe directly in your browser.**

## Screenshot

> ![https://raw.githubusercontent.com/kuranez/EU-Energy-Map/refs/heads/main/extra/images/screenshots/app.png](https://raw.githubusercontent.com/kuranez/EU-Energy-Map/refs/heads/main/extra/images/screenshots/app.png)

---


###  Example Charts
---

#### ➤ Renewable Energy Share Per Year
---
![https://raw.githubusercontent.com/kuranez/EU-Energy-Map/refs/heads/main/extra/images/screenshots/year_chart.png](https://raw.githubusercontent.com/kuranez/EU-Energy-Map/refs/heads/main/extra/images/screenshots/year_chart.png)

---
#### ➤ Renewable Energy Share Per Country
---
![https://raw.githubusercontent.com/kuranez/EU-Energy-Map/refs/heads/main/extra/images/screenshots/country_chart.png](https://raw.githubusercontent.com/kuranez/EU-Energy-Map/refs/heads/main/extra/images/screenshots/country_chart.png)

---
### Recent Changes
---

**Latest Data**

- **Updated to EuroStat data (2015–2024), while retaining historical data from 2004** for a broader perspective on renewable energy development in the European Union.

**Bar Charts**
- Unified display of **EU Total Average** across all charts, with a toggle option to show/hide it.
- Minor improvements to hover templates and trace labels.

**Map**
- Implemented hover templates displaying **country flags and data**.
- Recentered map and adjusted zoom.
- Added layout spacers for improved alignment.

**Description**
- Added basic **usage instructions** to the dashboard.
- Added emojis and graphics.

**Layout & Dashboard**
- Reorganized dashboard components for **better clarity and user experience**.
- Minor improvements to scaling.

**File Structure**
- Reorganization of file structure to me more **modular and easier to expand**.

---

## 📦 Python Dependencies

- **Core:** `os`, `json`, `pathlib`, `typing`

- **Data Handling:** `pandas`, `geopandas`

- **Visualization:** `plotly.express`, `plotly.graph_objects`, `plotly.io`

- **Dashboard UI:** `panel`


---

## 📊 Datasets

### 1. Renewable Energy Data (Eurostat)

- **File:** `nrg_ind_ren_linear.csv`

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


---

## 📁 File Structure

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
│   │
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
│   └── logo-500px.png                # Logo
|
└── geo/
    └── europe.geojson                # European country boundaries (GeoJSON)
```

---

## 📙 Documentation

Documentation is provided in `docs/` folder: [View documentation](docs/documentation.md)

---

## 📘 License

This project is open source and available under the **MIT License**.
You may modify, distribute, and use it freely in your own projects.

---

## 📓 Jupyter Notebook Version (Previous Release)

A standalone Jupyter Notebook version of the EU Energy Map dashboard is available from a previous release:

> [**Download Notebook Release v1.1**](https://github.com/kuranez/eu-energy-map/releases/tag/nb-1.1)

- Run the notebook locally to explore and visualize Eurostat renewable energy data without setting up the full web app.
- Includes interactive charts and geospatial mapping using the same datasets.
- Ideal for experimentation, prototyping, or educational use.

---

## 📕 Resources

> - [Holoviz Panel](https://panel.holoviz.org/) – A powerful Python framework for creating interactive web apps and dashboards, used for the UI in this project.
> - [Pandas](https://pandas.pydata.org/) – Essential for data manipulation and analysis, enabling efficient handling of Eurostat datasets.
> - [Geopandas](https://geopandas.org/) – Extends pandas to support geospatial data, making it easy to work with geographic boundaries and mapping.
> - [Jupyter](https://jupyter.org/) - An interactive environment for running Python code in notebooks, ideal for experimentation, documentation, and prototyping scripts.
> - [Docker Documentation](https://docs.docker.com/) -  Official guides for containerizing, deploying, and running this app consistently across different environments.

---

## 🔗 Related Projects

If you're working with Eurostat TSV datasets and need a tool for quick conversion to CSV, check out my companion project:

> ➡️ **[TSV-CSV Converter](https://github.com/kuranez/TSV-CSV-Converter)** – A lightweight utility to convert Eurostat-style `.tsv` files into clean `.csv` format.

---
