"""Data loading, validation, and transformation utilities."""

from .loader import load_datasets
from .transform import aggregate_by_subregion, compute_global_kpis, get_latest_by_year

__all__ = [
    "load_datasets",
    "aggregate_by_subregion",
    "compute_global_kpis",
    "get_latest_by_year",
]
