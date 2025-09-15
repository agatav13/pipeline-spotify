"""Extract step for pulling raw data from the Spotify API.

This module defines the ExtractSpotify class, which provides methods
to fetch artist, track, and album data from the Spotify API for use
in data pipelines.
"""

from typing import Any
from api.spotify_api import SpotifyAPI

from .base import PipelineStep


class ExtractSpotify(PipelineStep):
    """Extract step for pulling raw data from the Spotify API."""

    def __init__(
        self,
        artist_name: str | None = None,
        track_id: str | None = None,
        album_id: str | None = None,
    ) -> None:
        """
        Initialize the ExtractSpotify step.

        Args:
            artist_name (str | None, optional): Name of the artist to fetch.
            track_id (str | None, optional): ID of the track to fetch.
            album_id (str | None, optional): ID of the album to fetch.
        """
        self.artist_name = artist_name
        self.track_id = track_id
        self.album_id = album_id
        self.client = SpotifyAPI()
        self.client.get_token()

    def fetch_artist(
        self, artist_name: str, limit: int = 10, market: str | None = None
    ) -> list[dict[str, Any]]:
        """
        Fetch artist information from Spotify by name.

        Args:
            artist_name (str): Name of the artist to search for.
            limit (int, optional): Number of results to return. Defaults to 10.
            market (str | None, optional): Market code. Defaults to None.

        Returns:
            list[dict[str, Any]]: List of artist details.
        """
        result = self.client.search(
            artist_name, search_type=["artist"], limit=limit, market=market
        )
        artists = []
        for item in result["artists"]["items"]:
            artists.append(
                {
                    "id": item["id"],
                    "name": item["name"],
                    "genres": ", ".join(item["genres"]),
                    "followers": item["followers"]["total"],
                    "popularity": item["popularity"],
                }
            )
        return artists

    def fetch_track_by_artist_name(
        self, artist_name: str, market: str | None = "US"
    ) -> list[dict[str, Any]]:
        """
        Fetch top tracks for an artist by name.

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

        tracks = []
        for t in top_tracks["tracks"]:
            tracks.append(
                {
                    "id": t["id"],
                    "name": t["name"],
                    "popularity": t["popularity"],
                    "album": t["album"]["name"],
                    "release_date": t["album"]["release_date"],
                }
            )
        return tracks

    def fetch_track(
        self,
        *,
        artist_name: str | None = None,  # for top tracks
        track_id: str | None = None,
        track_name: str | None = None,  # for search by keyword
        limit: int = 10,
        market: str | None = "US",
    ) -> list[dict[str, Any]]:
        """
        Fetch track information by artist name, track ID, or track name.

        Args:
            artist_name (str | None, optional): Name of the artist.
            track_id (str | None, optional): ID of the track.
            track_name (str | None, optional): Name of the track.
            limit (int, optional): Number of results for search by name. Defaults to 10.
            market (str | None, optional): Market code. Defaults to "US".

        Returns:
            list[dict[str, Any]]: List of track details.

        Raises:
            ValueError: If more than one or none of the parameters are provided.
        """
        provided = [artist_name, track_id, track_name]
        if sum(x is not None for x in provided) != 1:
            raise ValueError("Provide either artist_name, track_id or track_title.")

        if artist_name:
            return self.fetch_track_by_artist_name(artist_name, market=market)
        if track_id:
            return self.fetch_track_by_id(track_id)
        if track_name:
            return self.fetch_track_by_name(track_name, limit=limit, market=market)

    def fetch_album(self, album_id):
        # TODO
        pass

    def run(self, data=None):
        if self.artist_name:
            return self.fetch_artist(self.artist_name)
        if self.track_id:
            return self.fetch_track(self.track_id)
        if self.album_id:
            return self.fetch_album(self.album_id)
        raise ValueError("No artist, track or album specified.")
