# Developer Setup

## Prerequisites

- Python 3.10+
- pip
- virtualenv support

## Environment Setup

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

## Run the Dashboard

```bash
python dashboard.py
```

Open <http://127.0.0.1:8050> in your browser.

## Package Layout

- climate_lens/config.py
- climate_lens/data/
- climate_lens/viz/
- dashboard.py

## Notebook Guidance

Use notebooks only for exploratory work. Runtime logic should be implemented in package modules and imported by the app.
