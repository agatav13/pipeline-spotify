# Spotify ETL Pipeline

This project is a simple ETL (Extract, Transform, Load) pipeline for Spotify data. It extracts information about new album releases using the Spotify Web API, transforms the raw data into a clean format, and loads it into a local SQLite database.

## Project Structure

```bash
├── api
│   └── spotify_api.py
├── db
│   ├── schema.sql
│   ├── setup_db.py
│   └── spotify.db
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
- Loads data into a SQLite database with conflict handling to avoid duplicates.
- Maintains relationships between albums and artists.

## Installation

This project uses [uv](https://github.com/astral-sh/uv) for dependency management.  
Make sure you have `uv` installed, then run:

```bash
uv sync
```

This will create a virtual environment and install all required dependencies from `pyproject.toml`.

## Configuration

Create a `.env` file in the project root with your Spotify API credentials:

```ini
SPOTIFY_CLIENT_ID=<your_client_id>
SPOTIFY_CLIENT_SECRET=<your_client_secret>
```

## Usage

To run the pipeline end-to-end:

```bash
python main.py
```

On first run, this will:

1. Create the SQLite database (`db/spotify.db`) using `db/schema.sql`.
2. Extract new album releases from the Spotify API.
3. Transform and clean the data.
4. Load the data into the database.

The next runs will update the database with new data without duplicating existing entries.

## Database Schema

The pipeline loads data into three tables:

- artist: Stores information about artists.
- album: Stores information about albums.
- album_artist: A join table linking albums and artists (many-to-many relationship).

Schema is defined in `db/schema.sql`.

## Testing

Run the test suite with:

```bash
pytest
```
