# Decisions Log

One entry per decision. Add the reason where one is marked `_add_`.

## 2026-11-16: Scope is collisions + weather only

- **Decision:** Use NYC Motor Vehicle Collisions (Socrata) and Open-Meteo historical weather only.
- **Considered and left out:** Traffic volume, road infrastructure, potholes.
- **Why:** _add_

## 2026-11-17: Build locally on Postgres first

- **Decision:** Build and test a small pipeline locally on Postgres, then move to AWS for the larger dataset.
- **Why:** Validate ingestion, joins, and transformations locally before running at scale on AWS.

## 2026-11-17: dlt is not used in the local build

- **Decision:** The local pipeline uses plain Python for extraction and loading; `dlt` is used in the main AWS pipeline.
- **Why:** Design the raw tables manually first to practice data modeling.

## 2026-11-17: 4-layer data architecture (`raw` → `stg` → `int` → `mart`)

- **Decision:** Structure the warehouse into four distinct layers:
              - **Warehouse layers:** `raw` → `stg` → `int` → `mart`

- **Why:** Writing the transformations in plain SQL first builds a clear understanding of the logic before wrapping them in `dbt`, and keeping identical 4-layer schemas across Postgres and S3 makes the cloud migration 1-to-1.

## 2026-11-22: Dashboard questions are set

- **Decision:** The season-wise and month-wise question lists are finalized for now (see `dashboard-questions.txt`). Weather conditions are derived from hourly weather parameters.
- **Why:** _add_

## 2026-11-22: Dashboard tool is Amazon QuickSight

- **Decision:** Build dashboards in Amazon QuickSight.
- **Why:** The 30-day free trial provides enough time to build and deploy the dashboards.

## 2026-11-22: Storage and query layer is S3 + Athena

- **Decision:** Store all four data layers (`raw`, `stg`, `int`, `mart`) in Amazon S3 and query them via Amazon Athena.
- **Why:** _add_

## 2026-11-22: Date range

- **Decision:**
  - **Main pipeline (1 year):** `2025-09-01` to `2026-08-31`
  - **Local prototype (2 months):** `2025-10-01` to `2025-11-30` (Oct–Nov 2025)
- **Why:** _add_

## 2026-11-22: Weather granularity is hourly

- **Decision:** Pull weather data at hourly resolution.
- **Why:** Hourly and daily were the only available options, and crash timestamps require hourly precision.

## 2026-11-22: Monthly ingestion with Kestra

- **Decision:** Kestra orchestrates monthly ingestion, incrementally loading only the latest completed month per run.
- **Run day:** _add_

## 2026-11-22: Entry point is `__main__.py`

- **Decision:** Start the pipeline from `src/nyc_motor_vehicle_pipeline/__main__.py` and execute via `uv run python -m nyc_motor_vehicle_pipeline`.

## 2026-11-24: Borough coordinates and staging timezone

- **Decision (Coordinates):** Pull hourly weather for all five NYC borough points rather than a single city-wide coordinate.

  | Borough | Latitude | Longitude |
  | :--- | :---: | :---: |
  | Manhattan | 40.7831 | -73.9712 |
  | Brooklyn | 40.6782 | -73.9442 |
  | Queens | 40.7282 | -73.7949 |
  | The Bronx | 40.8448 | -73.8648 |
  | Staten Island | 40.5795 | -74.1502 |

- **Why:** A test on `2023-09-29` (hourly, GMT) confirmed that temperature, precipitation, wind gusts, and weather codes vary across the five borough grid cells.

- **Decision (Timezone):** Keep NYC crashes in `America/New_York` at staging; keep Open-Meteo weather in `UTC` at staging, then convert weather to `America/New_York` (DST-aware) in the intermediate layer before joining.
- **Why:** UTC provides unambiguous hourly timestamps without Daylight Saving Time (DST) jumps. Per Open-Meteo documentation, requesting a named timezone applies a single fixed offset across the entire date range and ignores DST transitions, which would mislabel hours. Converting both sources to UTC in staging ensures collision and weather timestamps share a single consistent reference.

## 2026-11-26: ELT paradigm with 2 flattened tables in `raw`

- **Decision:** Follow an ELT approach with exactly 2 flattened source-aligned tables in the `raw` layer (`raw.mvc_crashes` and `raw.weather_hourly`), deferring star-schema splitting and transformations to `stg`, `int`, and `mart`.
- **Why:** Keeps raw ingestion decoupled from business modeling, mirrors how `dlt` lands one flattened table per API resource in S3/Athena later, and keeps source data unmodified for auditing.

## 2026-11-26: Primary keys and ingestion metadata in `raw`

- **Decision:**
  - **`raw.mvc_crashes`:** Use `collision_id` as the natural primary key.
  - **`raw.weather_hourly`:** Manually add a `borough` column during Python flattening (mapped by coordinate request order to uppercase Socrata names: `MANHATTAN`, `BROOKLYN`, `QUEENS`, `BRONX`, `STATEN ISLAND`) and use `(borough, time_utc)` as a composite primary key.
  - **Audit column:** Add `_ingested_at` to both `raw` tables.
- **Why:** Open-Meteo multi-coordinate responses omit `location_id` on the first element (`index 0`) and return `1–4` on the rest without borough names. Adding `borough` explicitly and enforcing `PRIMARY KEY (borough, time_utc)` guarantees grain uniqueness (`1 row per borough per UTC hour`) and supports idempotent upserts alongside `collision_id`.

## 2026-11-26: Weather code lookup table

- **Decision:** Create a separate static lookup/seed table mapping WMO `weather_code` integers to human-readable descriptions and grouped weather condition categories (e.g., `Clear`, `Fog`, `Rain`, `Snow`).
- **Why:** Keeps `raw.weather_hourly` raw while providing clean, human-readable weather labels and condition buckets for downstream analytics and QuickSight dashboards.
