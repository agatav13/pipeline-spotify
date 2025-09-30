from datetime import UTC, datetime

import psycopg2


def log_pipeline_run(
    database_url: str, operation: str, status: str, rows_added: int = None
) -> None:
    with psycopg2.connect(database_url) as conn:
        with conn.cursor() as cursor:
            cursor.execute("SELECT COUNT(*) FROM album;")
            total_albums = cursor.fetchone()[0]

            cursor.execute("SELECT COUNT(*) FROM artist;")
            total_artists = cursor.fetchone()[0]

            cursor.execute("SELECT COUNT(*) FROM album_artist;")
            total_album_artist = cursor.fetchone()[0]

            cursor.execute(
                """
                INSERT INTO pipeline_metrics (
                    run_at, operation, status, rows_added,
                    total_albums, total_artists, total_album_artist
                ) VALUES (%s, %s, %s, %s, %s, %s, %s)
                """,
                (
                    datetime.now(UTC),
                    operation,
                    status,
                    rows_added,
                    total_albums,
                    total_artists,
                    total_album_artist,
                ),
            )
