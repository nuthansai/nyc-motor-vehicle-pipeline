# NYC Motor Vehicle Collisions + Weather Pipeline

A data engineering pipeline that joins NYC Motor Vehicle Collisions (NYC Open Data / Socrata) with Open-Meteo historical hourly weather data.

**Status:** Early exploration. Both APIs have been tested at a surface level; pipeline implementation is next.

## Data Sources

| Source | What It Provides | Notes |
| :--- | :--- | :--- |
| **NYC Open Data (Socrata):** Motor Vehicle Collisions – Crashes | Police-reported crash events (one row per crash) | Dataset ID: `h9gi-nx95` *(verify before ingestion)* |
| **Open-Meteo:** Historical Weather API (`/v1/archive`) | Hourly reanalysis weather per borough | Variables: `temperature_2m`, `precipitation`, `rain`, `snowfall`, `wind_gusts_10m`, `weather_code` |

### About the Collisions Data

- **Grain:** One row per reported crash event (`collision_id`).
- **Coverage:** Police-reported collisions only. An MV-104AN report is required only when someone is injured or killed, or when property damage is at least $1,000.
- **Preliminary data:** Rows are preliminary and may be amended months later.
- **Timezone:** Source timestamps are in New York local time (`America/New_York`) and remain in `America/New_York` at staging.


## Scope

- **In scope:** Collisions + hourly weather across all 5 NYC boroughs.
- **Out of scope (for now):** Traffic volume, road infrastructure, potholes.

## Data Refresh Approach

- Collision records are loaded as a **snapshot** as of a recorded pull date; late amendments are not retroactively tracked.
- Because amendments typically occur months to a year later, no rolling lookback window is used.
- Both the pull date and Socrata's `count(*)` on that date are logged for reconciliation.

## Planned Stack

- **Local prototype:** Python extraction/loading, PostgreSQL, plain SQL transformations, then `dbt` models.
- **Main pipeline:** Terraform, Kestra, `dlt`, `dbt`, AWS (S3 + Athena), and Amazon QuickSight.
- **Warehouse layers:** `raw` → `stg` → `int` → `mart`

## Engineering Rules

- **Source verification:** Pulling the same date window twice must yield identical results, and ingested row counts must match Socrata's `count(*)`.
- **Timezone & DST handling:** Staging standardizes all timestamps to UTC; DST transition days are explicitly tested.
- **Idempotency:** Re-running any date window must produce identical, deduplicated results.

## Decisions Summary

All items below are finalized (see `DECISIONS.md` for full context and rationale):

- [x] **Scope:** Collisions + weather only
- [x] **Architecture:** 4 layers (`raw`, `stg`, `int`, `mart`)
- [x] **Analytics:** Season-wise and month-wise dashboard questions finalized
- [x] **Date ranges:** Main pipeline: `2025-09-01` to `2026-08-31` (1 year); Local prototype: `2025-10-01` to `2025-11-30` (2 months)
- [x] **Weather granularity:** Hourly, 5 borough coordinates
- [x] **Storage & query layer:** Amazon S3 + Amazon Athena
- [x] **BI & visualization:** Amazon QuickSight
- [x] **Orchestration & cadence:** Kestra monthly runs (incremental, latest completed month)
- [x] **Timezone strategy:** Crashes in `America/New_York` at staging; weather in `UTC` at staging and converted to `America/New_York` downstream


## Source Findings

*To be expanded as source validation tests are completed:*

| Attribute | Socrata (NYC MVC) | Open-Meteo (`/v1/archive`) |
| :--- | :--- | :--- |
| **Natural / Unique Key** | `collision_id` (per data dictionary) | `(borough, timestamp_utc)` |
| **Update Timestamp Field** | Not documented | N/A (reanalysis archive) |
| **Lookback Window** | None (snapshot approach) | None (5-day reanalysis lag from present) |
| **Source Timezone** | `America/New_York` (local time) | `UTC` (`GMT` default) |
| **Rate Limits & Terms** | Unthrottled with an App Token unless abusive; without a token, IP-based throttling applies (exact limit undocumented). | 10,000 API calls/day (non-commercial free tier) |
