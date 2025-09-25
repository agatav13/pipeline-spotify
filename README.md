# Spotify ETL Pipeline

This project is an **ETL** (Extract, Transform, Load) pipeline for Spotify data. It extracts information about new album releases using the **[Spotify Web API](https://developer.spotify.com/documentation/web-api)**, transforms the raw data into a clean format, and loads it into a **Postgres database hosted on [Supabase](https://supabase.com/)**.

## Project Structure

```bash
├── .github/workflows/
│   ├── etl.yaml
│   ├── lint.yaml
│   └── test.yaml
├── api
│   └── spotify_api.py
├── db
│   ├── schema.sql
├── pipeline
│   ├── extract.py
│   ├── load.py
│   ├── pipeline.py
│   └── transform.py
├── tests
│   ├── conftest.py
│   └── test_spotify_api.py
├── main.py
├── pyproject.toml
├── uv.lock
└── README.md
```

## Features

- Extracts new album releases from Spotify.
- Cleans and normalizes album and artist data.
- Loads data into **Supabase Postgres** with conflict handling to avoid duplicates.
- Maintains relationships between albums and artists.
- Automated daily runs using **GitHub Actions** (via `cron` schedule).
- Continuous integration: `ruff` linting and `pytest` testing on commits and pull requests.

## Installation

This project uses [uv](https://github.com/astral-sh/uv) for dependency management.  
Make sure you have `uv` installed, then run:

```bash
uv sync --group dev
```

This will create a virtual environment and install all required dependencies from `pyproject.toml`.

## Configuration

Create a `.env` file in the project root with your Spotify API credentials:

```ini
CLIENT_ID=<your_client_id>
CLIENT_SECRET=<your_client_secret>
DATABASE_URL=<your_database_url>
```

The `DATABASE_URL` should be copied from Supabase transaction pooler URI.

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

## Automation (CI/CD)

The project includes a GitHub Actions workflow (`.github/workflows/etl.yaml`) that:

- Runs the ETL pipeline every day at 09:00 UTC.
- Can also be triggered manually from the Actions tab.
- Uses GitHub Secrets for storing credentials (`CLIENT_ID`, `CLIENT_SECRET`, `DATABASE_URL`).
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
