# Climate Lens

Climate Lens is an interactive dashboard for analyzing global CO2, climate, and air-quality signals across countries and regions.

## What the Dashboard Includes

- Time-series views for CO2 and climate metrics by country.
- Global choropleth mapping for air-quality indicators.
- Comparative charts (distribution pie and top-10 ranking bars).
- Regional summary table with latest aggregated values by sub-region.

## Quick Start

1. Clone the repository:

```bash
git clone https://github.com/erdnuz/climate_lens
cd climate_lens
```

1. Create and activate a virtual environment:

```bash
python3 -m venv venv
source venv/bin/activate
```

1. Install dependencies:

```bash
pip install -r requirements.txt
```

1. Run the app:

```bash
python dashboard.py
```

1. Open [http://127.0.0.1:8050](http://127.0.0.1:8050).

## Project Structure

```text
climate_lens/
├── climate_lens/
│   ├── config.py
│   ├── data/
│   │   ├── loader.py
│   │   ├── transform.py
│   │   └── validator.py
│   └── viz/
│       └── figures.py
├── data/
├── notebooks/
│   ├── preprocessing.ipynb
│   ├── imputation.ipynb
│   ├── co2_forecast_analysis.ipynb
│   ├── co2_holt_forecast.ipynb
│   └── data_explore/
├── docs/
├── assets/
└── dashboard.py
```

## Architecture

- dashboard.py is the composition layer for layout and callbacks.
- climate_lens.data handles loading, schema checks, and transformations.
- climate_lens.viz handles Plotly figure construction.
- climate_lens.config centralizes labels, paths, and styling constants.

## Data Files Used at Runtime

- data/co2.csv
- data/climate.csv
- data/aq_imputed.csv
- data/country_map.csv

## Documentation

- Architecture: docs/ARCHITECTURE.md
- Data dictionary: docs/DATA_DICTIONARY.md
- Developer setup: docs/DEVELOPER_SETUP.md

## Notebook Usage

All notebooks and exploratory files are under notebooks/.
Application logic for runtime should be implemented in climate_lens/ modules and composed in dashboard.py.

## Data Provenance

Original raw datasets were pulled from Kaggle via kagglehub in the first cell of notebooks/preprocessing.ipynb.
