# Data Dictionary

## data/co2.csv

- country_code: ISO-3 country code.
- year: Observation year.
- co2: Total CO2 emissions.
- co2_per_capita: Per-capita CO2 emissions.
- population: Population estimate used in source dataset.

## data/climate.csv

- country_code: ISO-3 country code.
- year: Observation year.
- month: Observation month.
- R1: Rainfall metric used by this project as annual-average rainfall input after aggregation.
- temp_mean: Mean temperature.
- temp_max: Maximum temperature.
- temp_min: Minimum temperature.

## data/aq_imputed.csv

- country_code: ISO-3 country code.
- aq: Air quality index metric.
- PM2.5: Fine particulate concentration.
- PM10: Coarse particulate concentration.

## data/country_map.csv

- country_code: ISO-3 country code.
- country_name: Display country name.
- region: High-level geographic region.
- sub_region: Geographic sub-region.
- region_code: Region code value from source mapping.
- sub_region_code: Sub-region code value from source mapping.

## Notes

- Runtime merges are performed on country_code.
- Country codes are normalized to uppercase in the loader before merges.
- The dashboard's summary table is computed from latest-year values by sub-region.
