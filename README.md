# Spotify ETL Pipeline

This project is an **ETL** (Extract, Transform, Load) pipeline for Spotify data. It extracts information about new album releases using the **[Spotify Web API](https://developer.spotify.com/documentation/web-api)**, transforms the raw data into a clean format, loads it into a **Postgres database hosted on [Supabase](https://supabase.com/)**, , and then builds an **analytics layer with [dbt](https://docs.getdbt.com/)**.

## Project Structure

```bash
├── .github/workflows/         # GitHub Actions CI/CD
│   ├── etl.yaml               # Weekly ETL runs
│   ├── lint.yaml              # Ruff linting
│   └── test.yaml              # Pytest tests
├── api/
│   └── spotify_api.py         # Spotify API wrapper
├── db/
│   └── schema.sql             # Raw schema definition
├── pipeline/
│   ├── extract.py             # Extract step
│   ├── transform.py           # Transform step
│   ├── load.py                # Load step
│   ├── metrics.py             # Helper funtion for logging pipeline runs
│   └── pipeline.py            # Orchestration entrypoint
├── pipeline_spotify_dbt/      # dbt project
│   ├── models/
│   │   ├── staging/           # stg_ models (raw → clean)
│   │   └── analytics/         # dim_ / fact_ tables
│   └── schema.yml             # Sources + tests
├── tests/
│   ├── conftest.py
│   ├── test_extract.py
│   ├── test_load.py 
│   ├── test_spotify_api.py
│   └── test_transform.py
├── main.py
├── Makefile
├── pyproject.toml
├── uv.lock
└── README.md
```

## Features

- **ETL Pipeline**
    - Extracts new album releases from Spotify.
    - Cleans and normalizes album & artist data.
    - Loads into **Supabase Postgres** with conflict handling (no duplicates).
    - Maintains relationships between albums and artists.

- **Analytics Layer**
    - Built with **dbt** (staging → analytics/star schema).
    - Includes tests (unique keys, not null, referential integrity).
    - Generates browsable documentation (`dbt docs`).

- **Pipeline Observability**
    - `pipeline_metrics` table logs:
        - run timestamp
        - operation type
        - rows added
        - run status (success/failure)

- **Automation (CI/CD)**
    - Weekly ETL + dbt runs on **GitHub Actions**.
    - Linting with `ruff` and testing with `pytest` on push/PR.

## Installation

This project uses [uv](https://github.com/astral-sh/uv) for dependency management.  
Make sure you have `uv` installed, then run:

```bash
uv sync --group dev
```

This will create a virtual environment and install all required dependencies from `pyproject.toml`.

## Configuration

Create a `.env` file with credentials:

```ini
CLIENT_ID=<your_client_id>
CLIENT_SECRET=<your_client_secret>
DATABASE_URL=<your_database_url>
SUPABASE_HOST=...
SUPABASE_USER=...
SUPABASE_PASSWORD=...
SUPABASE_PORT=6543
SUPABASE_DB=postgres
SUPABASE_SCHEMA=public
```

The `DATABASE_URL` should be copied from Supabase transaction pooler URI. These values are also configured as GitHub Secrets for workflows.

## Usage

Run the pipeline locally with:

```bash
uv run main.py
```

This will:

1. Connect to your Supabase Postgres database.
2. Extract new album releases from the Spotify API.
3. Transform and clean the data.
4. Load the data into the database (avoiding duplicates).
5. Log run metadata into `pipeline_metrics`.

## Automation (CI/CD)

The project includes a GitHub Actions workflow (`.github/workflows/etl.yaml`) that:

- Runs the ETL pipeline along with `dbt` every week at 10:00 UTC.
- Can also be triggered manually from the Actions tab.
- Uses GitHub Secrets for storing credentials.
- Runs linting with `ruff` and tests with `pytest` on every push or pull request.

## Database Schema

The pipeline loads data into three tables:

- artist: Stores information about artists.
- album: Stores information about albums.
- album_artist: A join table linking albums and artists (many-to-many relationship).

Schema is defined in `db/schema.sql`.

## Testing

Run the test suite locally with:

```bash
uv run pytest
```

Format and lint code with:

```bash
uv run ruff format
uv run ruff check --fix
```

This ensures your code follows consistent style rules and passes all tests.
