"""Reusable transformations and KPI computations."""

from __future__ import annotations

from typing import Dict, Optional

import pandas as pd


def get_latest_by_year(df: pd.DataFrame) -> pd.DataFrame:
    """Return only rows from the latest year in the dataframe."""
    if "year" not in df.columns or df.empty:
        return df.copy()
    latest = df["year"].max()
    return df[df["year"] == latest].copy()


def _pct_change(current: float, previous: float) -> float:
    if not previous:
        return 0.0
    return (current - previous) / previous * 100


def compute_global_kpis(co2: pd.DataFrame, climate: pd.DataFrame, latest_year: Optional[int] = None) -> Dict[str, float]:
    """Compute headline KPI values and trend percentages."""
    if latest_year is None:
        latest_year = int(co2["year"].max())
    prev_year = latest_year - 1

    co2_data = co2.copy()
    co2_data["population"] = co2_data["co2"] / co2_data["co2_per_capita"]

    co2_latest = co2_data[co2_data["year"] == latest_year]
    co2_prev = co2_data[co2_data["year"] == prev_year]

    co2_pc_latest = co2_latest["co2"].sum() / co2_latest["population"].sum()
    co2_pc_prev = co2_prev["co2"].sum() / co2_prev["population"].sum()

    co2_total_latest = co2_latest["co2"].sum()
    co2_total_prev = co2_prev["co2"].sum()

    temp_max_latest = climate[climate["year"] == latest_year]["temp_max"].mean()
    temp_max_prev = climate[climate["year"] == prev_year]["temp_max"].mean()

    return {
        "latest_year": latest_year,
        "co2_pc_latest": co2_pc_latest,
        "co2_pc_trend": _pct_change(co2_pc_latest, co2_pc_prev),
        "co2_total_latest": co2_total_latest,
        "co2_total_trend": _pct_change(co2_total_latest, co2_total_prev),
        "temp_max_latest": temp_max_latest,
        "temp_max_trend": _pct_change(temp_max_latest, temp_max_prev),
    }


def aggregate_by_subregion(co2: pd.DataFrame, climate: pd.DataFrame, aq: pd.DataFrame) -> pd.DataFrame:
    """Aggregate latest values by sub-region for summary table."""
    co2_latest = get_latest_by_year(co2)
    climate_latest = get_latest_by_year(climate)
    aq_latest = get_latest_by_year(aq)

    co2_grouped = co2_latest.groupby("sub_region").agg({"co2": "mean", "co2_per_capita": "mean"}).reset_index()
    climate_grouped = climate_latest.groupby("sub_region").agg({"temp_min": "mean", "temp_max": "mean", "R1": "mean"}).reset_index()
    aq_grouped = aq_latest.groupby("sub_region").agg({"aq": "mean", "PM2.5": "mean", "PM10": "mean"}).reset_index()

    df = co2_grouped.merge(climate_grouped, on="sub_region", how="outer")
    df = df.merge(aq_grouped, on="sub_region", how="outer")

    df["co2_per_capita"] = df["co2_per_capita"] * 1000
    df["co2"] = df["co2"] / 1000

    for col in df.columns:
        if col != "sub_region":
            df[col] = df[col].round(2)

    return df.rename(
        columns={
            "sub_region": "Region",
            "co2": "CO2 Total (Mt)",
            "co2_per_capita": "CO2 per Capita (T)",
            "temp_min": "Min Temp (C)",
            "temp_max": "Max Temp (C)",
            "R1": "Avg Rainfall (mm)",
            "aq": "Air Quality Index",
            "PM2.5": "PM2.5",
            "PM10": "PM10",
        }
    )
