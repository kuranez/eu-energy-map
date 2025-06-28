# EU Energy Map Notebook Documentation

This document explains the main functions and workflow steps in the Jupyter Notebook version of the EU Energy Map project.

## Main Functions and Workflow

### 1. `iso2_to_flag(iso2_code)`
- **Purpose:** Converts a two-letter ISO2 country code (e.g., 'DE', 'FR', 'GR') to the corresponding flag emoji.
- **Usage:** Used for displaying country flags in tables, charts, and map hovers.
- **Logic:**
  - Accepts a string of length 2.
  - Returns the Unicode flag emoji or an empty string if invalid.

### 2. `add_country_flags(data)`
- **Purpose:** Adds a `Flag` column to a DataFrame using the `ISO2_Code` column.
- **Usage:** Ensures correct flag display, especially for Greece (EL→GR).
- **Logic:**
  - Expects a column `ISO2_Code` in the DataFrame.
  - Applies `iso2_to_flag` to each row.

### 3. `sort_columns(data, column_order)`
- **Purpose:** Reorders DataFrame columns for consistent display.
- **Usage:** Used before returning or displaying data tables.
- **Logic:**
  - Accepts a DataFrame and a list of column names.
  - Returns a DataFrame with columns in the specified order.

### 4. `load_data()`
- **Purpose:** Loads and merges the Eurostat CSV and GeoJSON data, processes columns, and adds flags.
- **Usage:** Main entry point for data preparation in the notebook.
- **Logic:**
  - Reads CSV and GeoJSON files.
  - Merges on country code (`CNTR_ID` and `geo`).
  - Renames columns for clarity.
  - Maps energy type codes to readable names.
  - Drops unnecessary columns.
  - Converts numeric columns and rounds values.
  - Adds `ISO2_Code` (EL→GR for flags), then adds `Flag` column.
  - Returns a DataFrame with columns: `Code`, `Flag`, `Country`, `Energy Type`, `Renewable Percentage`, `Year`, `geometry`.

### 5. `filter_data(data)`
- **Purpose:** Filters the merged data for EU countries and calculates EU averages.
- **Usage:** Used to prepare data for map and chart visualizations.
- **Logic:**
  - Filters for rows where `Code` is in the EU country set (including 'EL' for Greece).
  - Filters for 'Renewable Energy Total' energy type.
  - Groups by year to calculate EU average renewable percentage.
  - Returns filtered DataFrames for renewable data, EU total, selected year, and selected country.

### 6. `create_choropleth_map(df_year)`
- **Purpose:** Generates a Plotly choropleth map of renewable energy percentages by country.
- **Usage:** Main map visualization in the dashboard.
- **Logic:**
  - Uses `Code` for locations (must match GeoJSON `CNTR_ID`).
  - Uses `Flag` for hover display (from `ISO2_Code`).
  - Applies color normalization and custom color scale.

### 7. `create_bar_chart_year(df_year, year)`
- **Purpose:** Creates a bar chart of renewable energy by country for a given year.
- **Usage:** Yearly comparison of countries.
- **Logic:**
  - Sorts by renewable percentage.
  - Colors bars by value.
  - Adds EU average as a line.

### 8. `create_bar_chart_country(df_eu_total, df_country, country)`
- **Purpose:** Shows a country's renewable energy trend over time, with EU average for comparison.
- **Usage:** Country-level time series analysis.
- **Logic:**
  - Bar chart for selected country.
  - Line for EU average.

## Data Handling Notes
- **Greece (EL/GR):** Always keep 'EL' in `Code` for merging and plotting. Use `ISO2_Code` (EL→GR) for flag display.
- **Flags:** Always use the `Flag` column (generated from `ISO2_Code`) for display in tables, charts, and map hovers.
- **Column Order:** Use `sort_columns` to ensure consistent DataFrame structure.

## Versioning
- **v1.1.0:** Major refactor, improved documentation, modular code, and new flag logic.
- **v1.0.0:** Initial notebook version, basic workflow and dashboard.

---

For more details, see the notebook cells and markdown explanations in `eu-energy-map-nb-new.ipynb`.
