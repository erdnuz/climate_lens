"""Dataset loading and normalization utilities."""

from __future__ import annotations

from typing import Dict

import pandas as pd

from climate_lens.config import CO2_CUTOFF_YEAR, DATA_FILES
from climate_lens.data.validator import validate_dataset, validate_year_column


def _read_csv(path: str) -> pd.DataFrame:
    return pd.read_csv(path)


def _normalize_country_code(df: pd.DataFrame) -> pd.DataFrame:
    if "country_code" in df.columns:
        df["country_code"] = df["country_code"].astype(str).str.upper()
    return df


def load_datasets() -> Dict[str, pd.DataFrame]:
    """Load and validate all runtime datasets used by the dashboard."""
    datasets = {name: _normalize_country_code(_read_csv(path)) for name, path in DATA_FILES.items()}

    for name, df in datasets.items():
        validate_dataset(name, df)
        validate_year_column(name, df)

    countries = datasets["countries"]
    for key in ("aq", "climate", "co2"):
        datasets[key] = datasets[key].merge(countries, on="country_code", how="left")

    datasets["co2_forecast"] = datasets["co2"].copy()
    datasets["co2"] = datasets["co2"][datasets["co2"]["year"] < CO2_CUTOFF_YEAR].copy()
    return datasets
