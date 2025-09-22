import logging
from datetime import UTC, datetime
from typing import Any

logger = logging.getLogger(__name__)


class TransformSpotify:
    def clean_album(self, raw_album: dict[str, Any]) -> dict[str, Any] | None:
        if not raw_album.get("id") or not raw_album.get("name"):
            logger.warning("Skipping album with missing id or name: %s", raw_album)
            return None

        artists = []
        for artist in raw_album.get("artists", []):
            if artist.get("id") and artist.get("name"):
                artists.append(
                    {
                        "artist_id": artist["id"],
                        "artist_name": artist["name"],
                        "spotify_url": artist.get("external_urls", {}).get("spotify"),
                    }
                )

        images = raw_album.get("images", [])
        best_image = None
        if images:
            images_by_width = sorted(
                images, key=lambda x: x.get("width", 0), reverse=True
            )
            best_image = images_by_width[0].get("url")

        total_tracks = raw_album.get("total_tracks")
        try:
            total_tracks = int(total_tracks) if total_tracks is not None else None
        except (ValueError, TypeError):
            total_tracks = None

        release_date = raw_album.get("release_date")
        try:
            release_year = int(release_date.split("-")[0]) if release_date else None
        except (ValueError, IndexError):
            release_year = None

        logger.debug("Transformed album: %s", raw_album["name"])
        return {
            "album_id": raw_album["id"],
            "album_name": raw_album["name"].strip(),
            "album_type": raw_album.get("album_type", "unknown"),
            "artists": artists,
            "primary_artist_name": artists[0]["artist_name"] if artists else "Unknown",
            "primary_artist_id": artists[0]["artist_id"] if artists else None,
            "release_date": release_date,
            "release_year": release_year,
            "release_date_precision": raw_album.get("release_date_precision"),
            "total_tracks": total_tracks,
            "image_url": best_image,
            "spotify_url": raw_album.get("external_urls", {}).get("spotify"),
            "extracted_at": raw_album.get("extracted_at"),
            "extraction_type": raw_album.get("extraction_type"),
            "processed_at": datetime.now(UTC).isoformat(),
            "data_type": "album",
        }

    def transform_new_releases(
        self, raw_albums: list[dict[str, Any]]
    ) -> list[dict[str, Any]]:
        logger.info("Transforming %s albums...", len(raw_albums))
        transformed = []
        for raw_album in raw_albums:
            cleaned = self.clean_album(raw_album)
            if cleaned:
                transformed.append(cleaned)
        logger.info("Transformation complete. %s albums cleaned.", len(transformed))
        return transformed
