from datetime import UTC, datetime
from typing import Any

from api.spotify_api import SpotifyAPI


class ExtractSpotify:
    def __init__(self) -> None:
        self.client = SpotifyAPI()
        self.client.get_token()

    def extract_new_releases(self, limit: int = 20) -> list[dict[str, Any]]:
        """
        Extract new album releases.

        Args:
            limit: Between 1-50.
        """
        try:
            response = self.client.get_new_releases(limit=limit)
        except Exception as err:
            raise Exception("Failed to extract new releases") from err

        albums = response.get("albums", {}).get("items", [])
        for album in albums:
            album["extracted_at"] = datetime.now(UTC).isoformat()
            album["extraction_type"] = "new_releases"

        return albums
