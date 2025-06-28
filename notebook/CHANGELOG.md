# Changelog for EU Energy Map Notebook

All notable changes to the Jupyter Notebook version of the EU Energy Map project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/), and this notebook project uses semantic versioning.

## [1.1.0] - 2025-06-28
### Added
- New notebook version: `eu-energy-map-nb-new.ipynb` (formerly `documentation copy.ipynb`)
- Updated workflow and structure for improved readability and reproducibility
- Modularized code cells for data loading, filtering, mapping, and visualization
- Added detailed markdown documentation for each workflow step
- Improved flag handling and country code logic (EL/GR)
- Enhanced interactive widgets and dashboard layout
- Added color normalization and bar chart visualizations
- Provided step-by-step code for debugging and data exploration

### Changed
- Refactored notebook to match the current Python app logic for data merging and flag assignment
- Updated all code cells to use `ISO2_Code` for flag display, keeping `Code` as EL for Greece
- Improved documentation and code comments throughout

### Removed
- Deprecated or redundant cells from previous versions
- Old flag assignment logic using only `Code` column

---

## [1.0.0] - 2024-12-01
### Added
- Initial notebook version: `eu-energy-map-nb-old.ipynb` (formerly `documentation.ipynb`)
- Basic workflow for loading, merging, and visualizing Eurostat renewable energy data
- Initial dashboard and map visualization using Plotly and Panel
- Basic flag display and country code handling

---

**Note:** This changelog is for the notebook/documentation branch only. The main Python app has a separate changelog and release cycle.
