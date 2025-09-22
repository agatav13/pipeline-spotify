import logging
from datetime import UTC, datetime
from typing import Any

from api.spotify_api import SpotifyAPI

logger = logging.getLogger(__name__)


class ExtractSpotify:
    def __init__(self) -> None:
        self.client = SpotifyAPI()
        self.client.get_token()
        logger.info("ExtractSpotify initialized.")

    def extract_new_releases(self, limit: int = 20) -> list[dict[str, Any]]:
        """
        Extract new album releases.

        Args:
            limit: Between 1-50.
        """
        logger.info("Extracting new releases (limit=%s)...", limit)
        try:
            response = self.client.get_new_releases(limit=limit)
        except Exception as err:
            logger.exception("Failed to extract new releases.")
            raise Exception("Failed to extract new releases.") from err

        albums = response.get("albums", {}).get("items", [])
        logger.info("Extracted %s albums.", len(albums))
        for album in albums:
            album["extracted_at"] = datetime.now(UTC).isoformat()
            album["extraction_type"] = "new_releases"

        return albums
