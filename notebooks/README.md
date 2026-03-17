# Notebooks

This folder contains exploratory and research workflows only.

## Contents

- preprocessing.ipynb: raw data ingestion, harmonization, and initial table construction.
- imputation.ipynb: missing-value strategy and imputed air-quality outputs.
- co2_forecast_analysis.ipynb: exploratory forecasting analysis.
- co2_holt_forecast.ipynb: Holt-based forecast experimentation.
- data_explore/: intermediate exploration exports and working files.

## Boundary Rule

- Do not place production dashboard logic here.
- Runtime logic belongs in climate_lens/ modules and is consumed by dashboard.py.

## Source Provenance

The first code cell in preprocessing.ipynb downloads original datasets from Kaggle via kagglehub.
