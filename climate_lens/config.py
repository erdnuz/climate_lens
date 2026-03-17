"""Centralized application settings and constants."""

from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data"

DATA_FILES = {
    "aq": DATA_DIR / "aq_imputed.csv",
    "countries": DATA_DIR / "country_map.csv",
    "climate": DATA_DIR / "climate.csv",
    "co2": DATA_DIR / "co2.csv",
}

METRIC_LABELS = {
    "co2": "CO2 Total (T)",
    "co2_per_capita": "CO2 per Capita (T)",
    "temp_min": "Yearly Minimum Temperature (C)",
    "temp_max": "Yearly Maximum Temperature (C)",
    "R1": "Annual Average Rainfall (mm)",
}

POLLUTANT_OPTIONS = ["Air Quality Index", "PM2.5", "PM10"]

TOP10_OPTIONS = [
    {"label": "Air Quality Index", "value": "aq"},
    {"label": "PM2.5", "value": "PM2.5"},
    {"label": "PM10", "value": "PM10"},
    {"label": "Annual Rainfall", "value": "R1"},
    {"label": "CO2 per Capita", "value": "co2_per_capita"},
    {"label": "Total CO2", "value": "co2"},
]

THEME = {
    "page_bg": "#0f1116",
    "card_bg": "#1a1d24",
    "font": "#e0e6ed",
    "border": "#1f2937",
    "accent": "#4aa8ff",
    "danger": "#cc4444",
    "success": "#00aa55",
}

FIGURE_LAYOUT = {
    "paper_bgcolor": THEME["card_bg"],
    "plot_bgcolor": THEME["card_bg"],
    "font": {"color": THEME["font"]},
}

CO2_CUTOFF_YEAR = 2020
FORECAST_START_YEAR = 2019
DEFAULT_COUNTRIES = ["Canada", "United States"]
