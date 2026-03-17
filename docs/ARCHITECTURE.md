# Architecture

## Overview

Climate Lens is a Dash application with a modular Python package for configuration, data handling, and visualization logic.

The repository is intentionally separated into production runtime code and exploratory assets:

- Production runtime: climate_lens/, dashboard.py, data/, assets/
- Exploration and experiments: notebooks/
- Operational script area: scripts/

## Runtime Flow

1. dashboard.py starts the Dash app.
1. climate_lens.data.loader.load_datasets() loads and validates CSV inputs.
1. country metadata from data/country_map.csv is merged into analysis datasets.
1. climate_lens.data.transform computes KPI cards and summary table aggregates.
1. Dash callbacks call figure builders in climate_lens.viz.figures.
1. Plotly figures are rendered in the browser.

## Module Boundaries

- climate_lens/config.py
Purpose: Centralized constants, dataset paths, metric labels, and theme values.

- climate_lens/data/loader.py
Purpose: Load runtime datasets and normalize country codes.

- climate_lens/data/validator.py
Purpose: Enforce required columns and year typing checks.

- climate_lens/data/transform.py
Purpose: KPI and table aggregations, shared data transformation helpers.

- climate_lens/viz/figures.py
Purpose: Build Plotly figures for time series, choropleth, pie, and top-10 views.

- dashboard.py
Purpose: App composition, layout wiring, callback registration.

## Dependency Direction

- config -> data, viz, dashboard
- data -> dashboard
- viz -> dashboard
- dashboard is the runtime composition layer and should not hold business logic.

## Data Contracts

Expected runtime files:

- data/co2.csv
- data/climate.csv
- data/aq_imputed.csv
- data/country_map.csv

Validation currently checks required columns and year type for year-bearing tables.

## Notebook Policy

Notebooks are exploratory artifacts and are kept under notebooks/.
Production runtime logic should live in package modules under climate_lens/.
scripts/ is reserved for repeatable, non-notebook automation tasks.
