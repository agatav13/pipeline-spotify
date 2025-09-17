import base64
import os
from typing import Any

import requests
from dotenv import load_dotenv

load_dotenv()


class SpotifyAPI:
    TOKEN_URL: str = "https://accounts.spotify.com/api/token"  # noqa: S105
    BASE_URL: str = "https://api.spotify.com/v1"  # noqa: S105

    def __init__(self) -> None:
        self.client_id: str | None = os.getenv("CLIENT_ID")
        self.client_secret: str | None = os.getenv("CLIENT_SECRET")

        if not self.client_id or not self.client_secret:
            raise ValueError(
                "Missing CLIENT_ID or CLIENT_SECRET in environment variables."
            )

        creds: str = f"{self.client_id}:{self.client_secret}"
        self.client_creds_b64: str = base64.b64encode(creds.encode()).decode()

        self.access_token: str | None = None
        self.expires_in: int | None = None

    def get_token(self) -> str:
        token_data: dict[str, str] = {"grant_type": "client_credentials"}
        token_headers: dict[str, str] = {
            "Authorization": f"Basic {self.client_creds_b64}",
            "Content-Type": "application/x-www-form-urlencoded",
        }

        req = requests.post(
            url=self.TOKEN_URL, data=token_data, headers=token_headers, timeout=10
        )

        if req.status_code != 200:
            raise RuntimeError(f"Failed to get token: {req.status_code} {req.text}")

        data = req.json()
        self.access_token = data["access_token"]
        self.expires_in = data["expires_in"]

        return self.access_token

    def get_headers(self) -> dict[str, str]:
        if not self.access_token:
            raise RuntimeError("No access token. Call get_token() first.")
        return {
            "Authorization": f"Bearer {self.access_token}",
            "Content-Type": "application/json",
        }

    def make_request(self, endpoint: str, params: dict | None = None) -> dict[str, Any]:
        url: str = self.BASE_URL + endpoint
        headers: dict[str, str] = self.get_headers()

        req = requests.get(url=url, headers=headers, params=params, timeout=10)

        if req.status_code != 200:
            raise RuntimeError(f"Failed to make request: {req.status_code} {req.text}")

        return req.json()

    def search(
        self,
        query: str,
        search_type: list[str],
        limit: int = 10,
        market: str | None = None,
    ) -> dict[str, Any]:
        """
        https://developer.spotify.com/documentation/web-api/reference/search
        """
        search_type_str: str = ",".join(search_type)
        params: dict[str, Any] = {
            "q": query,
            "type": search_type_str,
            "limit": limit,
        }

        if market is not None:
            params["market"] = market

        return self.make_request("/search", params=params)

    def get_track(self, track_id: str, market: str | None = None) -> dict[str, Any]:
        """
        Get Spotify catalog information for a single track.
        https://developer.spotify.com/documentation/web-api/reference/get-track
        """
        params: dict[str, Any] = {}
        if market:
            params["market"] = market
        return self.make_request(f"/tracks/{track_id}", params=params)

    def get_several_tracks(
        self, track_ids: list[str], market: str | None = None
    ) -> dict[str, Any]:
        """
        Get Spotify catalog information for multiple tracks based on their IDs.
        https://developer.spotify.com/documentation/web-api/reference/get-several-tracks
        """
        ids_str = ",".join(track_ids)
        params: dict[str, Any] = {"ids": ids_str}
        if market:
            params["market"] = market
        return self.make_request("/tracks", params=params)

    def get_artist(self, artist_id: str) -> dict[str, Any]:
        """
        Get Spotify catalog information for a single artist.
        https://developer.spotify.com/documentation/web-api/reference/get-an-artist
        """
        return self.make_request(f"/artists/{artist_id}")

    def get_several_artists(self, artist_ids: list[str]) -> dict[str, Any]:
        """
        Get Spotify catalog information for multiple artists.
        Maximum: 50 IDs.
        https://developer.spotify.com/documentation/web-api/reference/get-multiple-artists
        """
        ids_str = ",".join(artist_ids)
        params: dict[str, Any] = {"ids": ids_str}
        return self.make_request("/artists", params=params)

    def get_artist_albums(
        self,
        artist_id: str,
        include_groups: list[str] | None = None,
        market: str | None = None,
        limit: int = 20,
        offset: int = 0,
    ) -> dict[str, Any]:
        """
        Get Spotify catalog information about an artist's albums.
        https://developer.spotify.com/documentation/web-api/reference/get-an-artists-albums

        include_groups can be: album, single, appears_on, compilation
        """
        params: dict[str, Any] = {"limit": limit, "offset": offset}
        if include_groups:
            params["include_groups"] = ",".join(include_groups)
        if market:
            params["market"] = market
        return self.make_request(f"/artists/{artist_id}/albums", params=params)

    def get_artist_top_tracks(self, artist_id: str, market: str) -> dict[str, Any]:
        """
        Get Spotify catalog information about an artist's top tracks by country.
        Market is required (ISO 3166-1 alpha-2 country code).
        https://developer.spotify.com/documentation/web-api/reference/get-an-artists-top-tracks
        """
        params: dict[str, Any] = {"market": market}
        return self.make_request(f"/artists/{artist_id}/top-tracks", params=params)

    def get_album(self, album_id: str, market: str | None = None) -> dict[str, Any]:
        """
        Get Spotify catalog information for a single album.
        https://developer.spotify.com/documentation/web-api/reference/get-an-album
        """
        params: dict[str, Any] = {}
        if market:
            params["market"] = market
        return self.make_request(f"/albums/{album_id}", params=params)

    def get_several_albums(
        self, album_ids: list[str], market: str | None = None
    ) -> dict[str, Any]:
        """
        Get Spotify catalog information for multiple albums.
        Maximum: 20 IDs.
        https://developer.spotify.com/documentation/web-api/reference/get-multiple-albums
        """
        ids_str = ",".join(album_ids)
        params: dict[str, Any] = {"ids": ids_str}
        if market:
            params["market"] = market
        return self.make_request("/albums", params=params)

    def get_album_tracks(
        self,
        album_id: str,
        market: str | None = None,
        limit: int = 20,
        offset: int = 0,
    ) -> dict[str, Any]:
        """
        Get Spotify catalog information about an album’s tracks.
        Supports pagination.
        https://developer.spotify.com/documentation/web-api/reference/get-an-albums-tracks
        """
        params: dict[str, Any] = {"limit": limit, "offset": offset}
        if market:
            params["market"] = market
        return self.make_request(f"/albums/{album_id}/tracks", params=params)

    def get_new_releases(
        self,
        limit: int = 20,
        offset: int = 0,
    ) -> dict[str, Any]:
        """
        Get a list of new album releases featured in Spotify.
        https://developer.spotify.com/documentation/web-api/reference/get-new-releases
        """
        params: dict[str, Any] = {"limit": limit, "offset": offset}
        return self.make_request("/browse/new-releases", params=params)
