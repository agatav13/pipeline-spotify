import logging
import sqlite3
from typing import Any

logger = logging.getLogger(__name__)


class LoadSpotify:
    def __init__(self, db_path: str) -> None:
        self.db_path = db_path
        logger.info("LoadSpotify initialized with DB path: %s", db_path)

    def load_album(self, clean_album: dict[str, Any]) -> None:
        logger.debug("Logging album into DB: %s", clean_album["album_name"])
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()

            cursor.execute(
                """
                INSERT INTO album (
                    album_id, album_name, album_type, release_date, release_year,
                    release_date_precision, total_tracks, image_url, spotify_url,
                    extracted_at, extraction_type, processed_at, data_type
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                ON CONFLICT(album_id) DO UPDATE SET
                    album_name = excluded.album_name,
                    album_type = excluded.album_type,
                    release_date = excluded.release_date,
                    release_year = excluded.release_year,
                    release_date_precision = excluded.release_date_precision,
                    total_tracks = excluded.total_tracks,
                    image_url = excluded.image_url,
                    spotify_url = excluded.spotify_url,
                    extracted_at = excluded.extracted_at,
                    extraction_type = excluded.extraction_type,
                    processed_at = excluded.processed_at,
                    data_type = excluded.data_type;
                """,
                (
                    clean_album["album_id"],
                    clean_album["album_name"],
                    clean_album["album_type"],
                    clean_album["release_date"],
                    clean_album["release_year"],
                    clean_album["release_date_precision"],
                    clean_album["total_tracks"],
                    clean_album["image_url"],
                    clean_album["spotify_url"],
                    clean_album["extracted_at"],
                    clean_album["extraction_type"],
                    clean_album["processed_at"],
                    clean_album["data_type"],
                ),
            )

            for artist in clean_album.get("artists", []):
                cursor.execute(
                    """
                    INSERT INTO artist (
                        artist_id, artist_name, spotify_url,
                        extracted_at, processed_at
                    ) VALUES (?, ?, ?, ?, ?)
                    ON CONFLICT(artist_id) DO UPDATE SET
                        artist_name = excluded.artist_name,
                        spotify_url = excluded.spotify_url,
                        extracted_at = excluded.extracted_at,
                        processed_at = excluded.processed_at;
                    """,
                    (
                        artist["artist_id"],
                        artist["artist_name"],
                        artist["spotify_url"],
                        clean_album["extracted_at"],
                        clean_album["processed_at"],
                    ),
                )

                cursor.execute(
                    """
                    INSERT INTO album_artist (
                        album_id, artist_id
                    ) VALUES (?, ?)
                    ON CONFLICT(album_id, artist_id) DO NOTHING;
                    """,
                    (
                        clean_album["album_id"],
                        artist["artist_id"],
                    ),
                )

        logger.info("Album loaded: %s", clean_album["album_name"])

    def load_new_releases(self, clean_albums: list[dict[str, Any]]) -> None:
        logger.info("Loading %s albums into DB...", len(clean_albums))
        for clean_album in clean_albums:
            self.load_album(clean_album=clean_album)
        logger.info("Finished loading albums.")
