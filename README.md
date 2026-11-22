# NYC Motor Vehicle Collisions + Weather Pipeline

A data engineering project that joins NYC Motor Vehicle Collisions (NYC Open Data / Socrata) with Open-Meteo historical weather.

**Status:** early exploration. Both APIs have been explored at a surface level. No pipeline is built yet.

## Sources

| Source | What it provides | Notes |
|---|---|---|
| NYC Open Data (Socrata): Motor Vehicle Collisions, Crashes | Police-reported crash events, one row per crash | Dataset ID: _TODO_ |
| Open-Meteo Historical Weather API | Hourly historical weather | Variables: _TODO_ |

### About the collisions data

- **Grain:** one row per crash event.
- **Coverage:** police-reported collisions only. A police report (MV-104AN) is required when someone is injured or killed, or when damage is at least $1000. This is not every collision in NYC.
- **Preliminary data:** per the dataset description, rows are preliminary and may change when reports are amended.
- **Timezone:** crash date/time are in New York local time.

## Scope

- In scope: collisions + weather.
- Considered and left out for now: traffic volume, road infrastructure, potholes.

## Data refresh approach

- The collisions data is loaded as a **snapshot** as of a recorded pull date. Later amendments to source rows are not tracked.
- Amendments are expected to appear only months to a year later, so no short lookback window is used.
- The pull date and the Socrata `count(*)` on that date are recorded for reconciliation.

## Planned stack

- **Local build:** Python extraction, Postgres, plain SQL first, then dbt models.
- **Main pipeline:** Terraform, Kestra, dlt, dbt, AWS (S3 plus a query layer).
- Not used: Spark, Kafka, Airflow.

## Engineering rules

- Test each source before building on it: the same window pulled twice must give identical results, and row counts are compared against Socrata's own `count(*)`.
- Staging uses UTC (NY local times are converted); DST transition days are tested.
- Re-running a date window must give identical, deduplicated results (idempotent loads).

## Open decisions

- [ ] Dashboard questions
- [ ] Date range
- [ ] Weather granularity
- [ ] Cadence and lag
- [ ] Storage and query layer
- [ ] Budget cap
- [ ] Dashboard tool

## Source findings

To be filled in as the source tests are run:

| Item | Socrata | Open-Meteo |
|---|---|---|
| Unique key | collision_id per data dictionary | n/a |
| Update field | Not documented | n/a |
| Lookback window | None (snapshot approach, see above) | none |
| Timestamp / timezone handling | NY local time | UTC and Timezone offset can be used |
| Rate limits / terms | Requests with an application token are not throttled unless judged abusive or malicious (per Socrata docs). Limits without a token: Based on IP address for a given time period and exact limit not documented | 10000 daily |

## Repository layout

_TODO: add once the code structure exists._
