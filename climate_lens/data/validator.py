"""Validation helpers for required climate-lens datasets."""

from __future__ import annotations

import pandas as pd


REQUIRED_COLUMNS = {
    "aq": {"country_code", "aq", "PM2.5", "PM10"},
    "countries": {"country_code", "country_name", "sub_region"},
    "climate": {"country_code", "year", "temp_min", "temp_max", "R1"},
    "co2": {"country_code", "year", "co2", "co2_per_capita"},
}


def validate_dataset(name: str, df: pd.DataFrame) -> None:
    """Validate dataset schema and raise a helpful error on mismatch."""
    expected = REQUIRED_COLUMNS.get(name)
    if expected is None:
        return
    missing = expected - set(df.columns)
    if missing:
        missing_cols = ", ".join(sorted(missing))
        raise ValueError(f"Dataset '{name}' is missing required columns: {missing_cols}")


def validate_year_column(name: str, df: pd.DataFrame) -> None:
    """Ensure year values are numeric where year is required."""
    if "year" not in df.columns:
        return
    if not pd.api.types.is_numeric_dtype(df["year"]):
        raise ValueError(f"Dataset '{name}' has non-numeric 'year' values")
