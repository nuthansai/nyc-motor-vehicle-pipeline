# NYC Motor Vehicle Collisions + Weather Pipeline

A data engineering pipeline that joins NYC Motor Vehicle Collisions (NYC Open Data / Socrata) with Open-Meteo historical hourly weather data to analyze crash frequency, severity, and weather conditions across all five NYC boroughs.

**Status:** Phase 1 complete — Local raw ingestion into PostgreSQL (`raw.mvc_crashes` and `raw.weather_hourly`) via Docker Compose is implemented and verified. Next: `stg` → `int` → `mart` SQL and `dbt` transformations.

## Data Sources

| Source | What It Provides | Notes |
| :--- | :--- | :--- |
| **NYC Open Data (Socrata):** Motor Vehicle Collisions – Crashes | Police-reported crash events (one row per crash) | Dataset ID: `h9gi-nx95` (verified) |
| **Open-Meteo:** Historical Weather API (`/v1/archive`) | Hourly reanalysis weather per borough | Variables: `temperature_2m`, `precipitation`, `rain`, `snowfall`, `wind_gusts_10m`, `weather_code` |

## Local Setup & Running the Pipeline

1. **Configure environment variables:**
   Create a `.env` file at the project root with your PostgreSQL and pgAdmin credentials (`POSTGRES_USER`, `POSTGRES_PASSWORD`, `POSTGRES_DB`, `DB_HOST`, `DB_PORT`, `PGADMIN_DEFAULT_EMAIL`, `PGADMIN_DEFAULT_PASSWORD`) and optional `NYC_OPEN_DATA_APP_TOKEN`.
2. **Start PostgreSQL & pgAdmin:**
   ```bash
   docker compose up -d
   ```
   *(Automatically initializes the `raw` schema and tables from `sql/create_tables.sql` on first startup).*
3. **Install dependencies & run the local load:**
   ```bash
   uv sync
   uv run python -m nyc_motor_vehicle_pipeline
   ```


### About the Collisions Data

- **Grain:** One row per reported crash event (`collision_id`).
- **Coverage:** Police-reported collisions only. An MV-104AN report is required only when someone is injured or killed, or when property damage is at least $1,000.
- **Preliminary data:** Rows are preliminary and may be amended months later.
- **Timezone:** Source timestamps (`crash_date`, `crash_time`) are in New York local time (`America/New_York`) and remain in `America/New_York` at staging.

## Scope

- **In scope:** Collisions + hourly weather across all 5 NYC boroughs (`MANHATTAN`, `BROOKLYN`, `QUEENS`, `BRONX`, `STATEN ISLAND`).
- **Out of scope (for now):** Traffic volume, road infrastructure, potholes.

## Data Refresh Approach

- Collision records are loaded as a **snapshot** as of a recorded pull date; late amendments are not retroactively tracked.
- Because amendments typically occur months to a year later, no rolling lookback window is used.
- Both the pull date and Socrata's `count(*)` on that date are logged for reconciliation.

## Stack & Warehouse Layers

- **Local prototype:** Python (`uv`, `pandas`, `SQLAlchemy`, `psycopg`), Docker Compose (PostgreSQL 18 + pgAdmin), plain SQL transformations, and `dbt`.
- **Main pipeline:** Terraform, Kestra, `dlt`, `dbt`, AWS (S3 + Athena), and Amazon QuickSight.
- **Warehouse layers:** `raw` → `stg` → `int` → `mart`

## Engineering Rules

- **Source verification:** Pulling the same date window twice must yield identical results, and ingested row counts must match Socrata's `count(*)`.
- **Timezone & DST handling:** Source timezones are preserved in `raw` and `stg` (`America/New_York` for crashes, `UTC` for weather); weather timestamps are converted to `America/New_York` in `int` before joining, with DST transition days explicitly tested.
- **Idempotency:** Re-running any date window in the production pipeline must produce identical, deduplicated results.

## Current Progress

- [x] **API exploration & validation:** Confirmed schemas, pagination, keys, and borough coordinate order (`h9gi-nx95` and Open-Meteo `/v1/archive`).
- [x] **Local database setup:** Configured PostgreSQL and pgAdmin via `docker-compose.yaml` with automated `raw` schema/table initialization (`sql/create_tables.sql`).
- [x] **Extraction & flattening:** Built modular Python extractors and flatteners (`mvc` and `open_meteo` packages).
- [x] **Raw ingestion:** Loaded local prototype window (`2025-10-01` to `2025-11-30`) into `raw.mvc_crashes` and `raw.weather_hourly` (7,320 borough-hour rows).
- [ ] **Transformations (`stg` → `int` → `mart`):** Build SQL and `dbt` models to clean, timezone-align, join, and aggregate crash and weather data.
- [ ] **Cloud & orchestration:** Migrate ingestion and transformations to Terraform, Kestra, `dlt`, AWS S3 + Athena, and QuickSight (`2025-09-01` to `2026-08-31`).

## Decisions Summary

All items below are finalized (see `decisions.md` for full context and rationale):

- [x] **Scope:** Collisions + weather only
- [x] **Architecture:** 4 layers (`raw`, `stg`, `int`, `mart`)
- [x] **Analytics:** Season-wise and month-wise dashboard questions finalized (`dashboard-questions.txt`)
- [x] **Date ranges:** Main pipeline: `2025-09-01` to `2026-08-31` (1 year); Local prototype: `2025-10-01` to `2025-11-30` (2 months)
- [x] **Weather granularity:** Hourly, 5 borough coordinates
- [x] **Storage & query layer:** Amazon S3 + Amazon Athena
- [x] **BI & visualization:** Amazon QuickSight
- [x] **Orchestration & cadence:** Kestra monthly runs (incremental, latest completed month)
- [x] **Timezone strategy:** Crashes in `America/New_York` at staging; weather in `UTC` at staging and converted to `America/New_York` downstream

## Source Findings

| Attribute | Socrata (NYC MVC) | Open-Meteo (`/v1/archive`) |
| :--- | :--- | :--- |
| **Natural / Unique Key** | `collision_id` (per data dictionary) | `(borough, hourly_time)` |
| **Update Timestamp Field** | Not documented (Socrata system `:updated_at` excluded) | N/A (reanalysis archive) |
| **Lookback Window** | None (snapshot approach) | None (5-day reanalysis lag from present) |
| **Source Timezone** | `America/New_York` (local time) | `UTC` (`GMT` default) |
| **Rate Limits & Terms** | Unthrottled with an App Token unless abusive; without a token, IP-based throttling applies. | 10,000 API calls/day (non-commercial free tier) |
