import logging
from typing import Any

import psycopg2

from pipeline.metrics import log_pipeline_run

logger = logging.getLogger(__name__)


class LoadSpotify:
    def __init__(self, database_url: str) -> None:
        self.database_url = database_url
        logger.info("LoadSpotify initialized with database URL.")

    def load_album(self, clean_album: dict[str, Any]) -> None:
        logger.debug("Logging album into DB: %s", clean_album["album_name"])
        with psycopg2.connect(self.database_url) as conn:
            with conn.cursor() as cursor:
                cursor.execute(
                    """
                    INSERT INTO album (
                        album_id, album_name, album_type, release_date, release_year,
                        release_date_precision, total_tracks, image_url, spotify_url,
                        extracted_at, extraction_type, processed_at, data_type
                    ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                    ON CONFLICT (album_id) DO UPDATE SET
                        album_name = EXCLUDED.album_name,
                        album_type = EXCLUDED.album_type,
                        release_date = EXCLUDED.release_date,
                        release_year = EXCLUDED.release_year,
                        release_date_precision = EXCLUDED.release_date_precision,
                        total_tracks = EXCLUDED.total_tracks,
                        image_url = EXCLUDED.image_url,
                        spotify_url = EXCLUDED.spotify_url,
                        extracted_at = EXCLUDED.extracted_at,
                        extraction_type = EXCLUDED.extraction_type,
                        processed_at = EXCLUDED.processed_at,
                        data_type = EXCLUDED.data_type;
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
                        ) VALUES (%s, %s, %s, %s, %s)
                        ON CONFLICT (artist_id) DO UPDATE SET
                            artist_name = EXCLUDED.artist_name,
                            spotify_url = EXCLUDED.spotify_url,
                            extracted_at = EXCLUDED.extracted_at,
                            processed_at = EXCLUDED.processed_at;
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
                        ) VALUES (%s, %s)
                        ON CONFLICT (album_id, artist_id) DO NOTHING;
                        """,
                        (
                            clean_album["album_id"],
                            artist["artist_id"],
                        ),
                    )

        logger.info("Album loaded: %s", clean_album["album_name"])

    def load_new_releases(self, clean_albums: list[dict[str, Any]]) -> None:
        logger.info("Loading %s albums into DB...", len(clean_albums))
        try:
            for clean_album in clean_albums:
                self.load_album(clean_album=clean_album)
            log_pipeline_run(
                database_url=self.database_url,
                operation="load_new_releases",
                status="success",
                rows_added=len(clean_albums),
            )
            logger.info("Finished loading albums.")
        except Exception as e:
            log_pipeline_run(
                database_url=self.database_url,
                operation="load_new_releases",
                status="failure",
                rows_added=len(clean_albums),
            )
            logger.error("Pipeline failes: %s", e)
            raise
