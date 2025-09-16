"""Extract step for pulling raw data from the Spotify API.

This module defines the ExtractSpotify class, which provides methods
to fetch artist, track, and album data from the Spotify API for use
in data pipelines.
"""

from typing import Any

from api.spotify_api import SpotifyAPI

from .base import PipelineStep


class ExtractSpotify(PipelineStep):
    """Pipeline step to extract raw data from Spotify."""

    def __init__(self) -> None:
        """Initialize the ExtractSpotify step.

        The client is authenticated here.
        """
        self.client = SpotifyAPI()
        self.client.get_token()

    def fetch_artist(
        self, artist_name: str, limit: int = 10, market: str | None = None
    ) -> list[dict[str, Any]]:
        """Fetch artist information from Spotify by name.

        Args:
            artist_name (str): Name of the artist to search for.
            limit (int, optional): Maximum number of results to return. Defaults to 10.
            market (str | None, optional): Market code. Defaults to None.

        Returns:
            list[dict[str, Any]]: List of artist details.
        """
        result = self.client.search(
            artist_name, search_type=["artist"], limit=limit, market=market
        )
        return [
            {
                "id": item["id"],
                "name": item["name"],
                "genres": ", ".join(item["genres"]),
                "followers": item["followers"]["total"],
                "popularity": item["popularity"],
            }
            for item in result["artists"]["items"]
        ]

    def fetch_track_by_artist_name(
        self, artist_name: str, market: str | None = "US"
    ) -> list[dict[str, Any]]:
        """Fetch top tracks for an artist by name.

        Args:
            artist_name (str): Name of the artist.
            market (str | None, optional): Market code. Defaults to "US".

        Returns:
            list[dict[str, Any]]: List of track details.
        """
        artist_result = self.client.search(
            artist_name, ["artist"], limit=1, market=market
        )
        items = artist_result["artists"]["items"]
        if not items:
            return []

        artist_id = items[0]["id"]
        top_tracks = self.client.get_artist_top_tracks(artist_id, market=market)

        return [
            {
                "id": t["id"],
                "name": t["name"],
                "popularity": t["popularity"],
                "album": t["album"]["name"],
                "release_date": t["album"]["release_date"],
            }
            for t in top_tracks["tracks"]
        ]

    def fetch_track_by_id(self, track_id: str) -> list[dict[str, Any]]:
        """Fetch a single track by its Spotify ID.

        Args:
            track_id (str): Spotify track ID.

        Returns:
            list[dict[str, Any]]: List containing one track detail dictionary.
        """
        result = self.client.get_track(track_id)
        track = {
            "id": result["id"],
            "name": result["name"],
            "popularity": result["popularity"],
            "album": result["album"]["name"],
            "release_date": result["album"]["release_date"],
        }
        return [track]

    def fetch_track_by_name(
        self, track_name: str, limit: int = 10, market: str | None = "US"
    ) -> list[dict[str, Any]]:
        """Fetch tracks by name keyword search.

        Args:
            track_name (str): Name keyword for track search.
            limit (int, optional): Maximum number of results to return. Defaults to 10.
            market (str | None, optional): Market code. Defaults to "US".

        Returns:
            list[dict[str, Any]]: List of track details.
        """
        result = self.client.search(track_name, ["track"], limit=limit, market=market)
        return [
            {
                "id": track["id"],
                "name": track["name"],
                "popularity": track["popularity"],
                "album": track["album"]["name"],
                "release_date": track["album"]["release_date"],
            }
            for track in result["tracks"]["items"]
        ]

    def fetch_track(
        self,
        *,
        artist_name: str | None = None,  # for top tracks
        track_id: str | None = None,
        track_name: str | None = None,  # for search by keyword
        limit: int = 10,
        market: str | None = "US",
    ) -> list[dict[str, Any]]:
        """Fetch track information using one of the parameters:
        artist_name, track_id, or track_name.

        Args:
            artist_name (str | None, optional): Name of the artist (for top tracks).
            track_id (str | None, optional): Spotify track ID.
            track_name (str | None, optional): Name keyword for track search.
            limit (int, optional): Maximum number of results when searching by name.
            market (str | None, optional): Market code. Defaults to "US".

        Returns:
            list[dict[str, Any]]: List of track details.

        Raises:
            ValueError: If none or more than one parameter is provided.
        """
        provided = [artist_name, track_id, track_name]
        if sum(x is not None for x in provided) != 1:
            raise ValueError(
                "Provide exactly one of artist_name, track_id, or track_name."
            )

        if artist_name:
            return self.fetch_track_by_artist_name(artist_name, market=market)
        if track_id:
            return self.fetch_track_by_id(track_id)
        if track_name:
            return self.fetch_track_by_name(track_name, limit=limit, market=market)
        return None

    def fetch_album_by_artist_name(
        self, artist_name: str, limit: int = 10, market: str | None = "US"
    ) -> list[dict[str, Any]]:
        """Fetch top albums for an artist by name.

        Args:
            artist_name (str): Name of the artist.
            limit (int, optional): Maximum number of albums to return. Defaults to 10.
            market (str | None, optional): Market code. Defaults to "US".

        Returns:
            list[dict[str, Any]]: List of album details.
        """
        artist_result = self.client.search(
            artist_name, ["artist"], limit=1, market=market
        )
        items = artist_result["artists"]["items"]
        if not items:
            return []

        artist_id = items[0]["id"]
        albums_result = self.client.get_artist_top_albums(
            artist_id, limit=limit, market=market
        )

        return [
            {
                "id": a["id"],
                "name": a["name"],
                "release_date": a["release_date"],
                "total_tracks": a["total_tracks"],
                "album_type": a["album_type"],
            }
            for a in albums_result["items"]
        ]

    def fetch_album_by_id(self, album_id: str) -> list[dict[str, Any]]:
        """Fetch a single album by its Spotify ID.

        Args:
            album_id (str): Spotify album ID.

        Returns:
            list[dict[str, Any]]: List containing one album detail dictionary.
        """
        result = self.client.get_album(album_id)
        album = {
            "id": result["id"],
            "name": result["name"],
            "release_date": result["release_date"],
            "total_tracks": result["total_tracks"],
            "album_type": result["album_type"],
        }
        return [album]

    def fetch_album_by_name(
        self, album_name: str, limit: int = 10, market: str | None = "US"
    ) -> list[dict[str, Any]]:
        """Search albums by name keyword.

        Args:
            album_name (str): Album name keyword.
            limit (int, optional): Maximum number of albums to return. Defaults to 10.
            market (str | None, optional): Market code. Defaults to "US".

        Returns:
            list[dict[str, Any]]: List of album details.
        """
        result = self.client.search(album_name, ["album"], limit=limit, market=market)
        return [
            {
                "id": a["id"],
                "name": a["name"],
                "release_date": a["release_date"],
                "total_tracks": a["total_tracks"],
                "album_type": a["album_type"],
            }
            for a in result["albums"]["items"]
        ]

    def fetch_album(
        self,
        *,
        artist_name: str | None = None,
        album_id: str | None = None,
        album_name: str | None = None,
        limit: int = 10,
        market: str | None = "US",
    ) -> list[dict[str, Any]]:
        """Fetch album information using one of the parameters:
        artist_name (top albums), album_id, or album_name (search).

        Args:
            artist_name (str | None, optional): Name of the artist (for top albums).
            album_id (str | None, optional): Spotify album ID.
            album_name (str | None, optional): Name keyword for album search.
            limit (int): Maximum number of results when searching by name.
            market (str | None, optional): Market code. Defaults to "US".

        Returns:
            list[dict[str, Any]]: List of album details.

        Raises:
            ValueError: If none or more than one parameter is provided.
        """
        provided = [artist_name, album_id, album_name]
        if sum(x is not None for x in provided) != 1:
            raise ValueError(
                "Provide exactly one of artist_name, album_id, or album_name."
            )

        if artist_name:
            return self.fetch_album_by_artist_name(
                artist_name, limit=limit, market=market
            )
        if album_id:
            return self.fetch_album_by_id(album_id)
        return self.fetch_album_by_name(album_name, limit=limit, market=market)

    def run(
        self,
        entity_type: str,  # "artist", "track", or "album"
        *,
        artist_name: str | None = None,
        track_id: str | None = None,
        track_name: str | None = None,
        album_id: str | None = None,
        album_name: str | None = None,
        limit: int = 10,
        market: str | None = "US",
    ) -> list[dict[str, Any]]:
        """Unified run method to fetch data for the specified entity type.

        Args:
            entity_type (str): One of "artist", "track", or "album".
            artist_name (str | None, optional): Name of the artist.
            track_id (str | None, optional): Spotify track ID.
            track_name (str | None, optional): Name keyword for track search.
            album_id (str | None, optional): Spotify album ID.
            album_name (str | None, optional): Name keyword for album search.
            limit (int, optional): Maximum number of results to return. Defaults to 10.
            market (str | None, optional): Market code. Defaults to "US".

        Returns:
            list[dict[str, Any]]: Fetched data.

        Raises:
            ValueError: If required parameters for the entity type are missing.
        """
        if entity_type == "artist":
            if not artist_name:
                raise ValueError("artist_name is required for fetching artist info")
            return self.fetch_artist(artist_name, limit=limit, market=market)

        if entity_type == "track":
            if not any([track_id, track_name, artist_name]):
                raise ValueError(
                    "track_id, track_name, or artist_name is required for fetching tracks"  # noqa: E501
                )
            return self.fetch_track(
                artist_name=artist_name,
                track_id=track_id,
                track_name=track_name,
                limit=limit,
                market=market,
            )

        if entity_type == "album":
            if not any([album_id, album_name, artist_name]):
                raise ValueError(
                    "album_id, album_name, or artist_name is required for fetching albums"  # noqa: E501
                )
            return self.fetch_album(
                artist_name=artist_name,
                album_id=album_id,
                album_name=album_name,
                limit=limit,
                market=market,
            )

        raise ValueError(f"Unknown entity_type: {entity_type}")
