"""Class for handling Spotify API.

Provides the SpotifyAPI client for authentication and resource access.
"""

import base64
import os
from typing import Any

import requests
from dotenv import load_dotenv

load_dotenv()


class SpotifyAPI:
    """Client for interacting with the Spotify Web API.

    This class handles authentication and provides helper methods
    for accessing common Spotify endpoints such as tracks, artists,
    albums and search.
    """

    TOKEN_URL: str = "https://accounts.spotify.com/api/token"  # noqa: S105
    BASE_URL: str = "https://api.spotify.com"  # noqa: S105

    def __init__(self) -> None:
        """Initialize the SpotifyAPI client.

        Loads client credentials from environment variables
        (`CLIENT_ID` and `CLIENT_SECRET`) and prepares the base64
        encoded credentials for authentication.

        Raises:
            ValueError: If `CLIENT_ID` or `CLIENT_SECRET` are missing.
        """
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
        """Obtain an access token using Client Credentials Flow.

        Returns:
            str: Access token string.

        Raises:
            RuntimeError: If the token request fails.
        """
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
        """Build headers for authorized Spotify API requests.

        Returns:
            Dict[str, str]: Headers including the Bearer access token.

        Raises:
            RuntimeError: If `get_token()` has not been called.
        """
        if not self.access_token:
            raise RuntimeError("No access token. Call get_token() first.")
        return {
            "Authorization": f"Bearer {self.access_token}",
            "Content-Type": "application/json",
        }

    def make_request(self, endpoint: str, params: dict | None = None) -> dict[str, Any]:
        """Make a GET request to the Spotify API.

        Args:
            endpoint (str): API endpoint (e.g., "/v1/tracks/{id}").
            params (dict | None): Optional query parameters.

        Returns:
            Dict[str, Any]: JSON response from the Spotify API.

        Raises:
            RuntimeError: If the request fails.
        """
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
        """Search for tracks, artists, albums or playlists.

        Args:
            query (str): Search query string (e.g., "Taylor Swift").
            search_type (List[str]): Types to search (e.g., ["track", "album"]).
            limit (int, optional): Number of results to return. Defaults to 10.
            market (str | None, optional): Market code (e.g., "US", "PL").
                Defaults to None.

        Returns:
            Dict[str, Any]: JSON response containing search results.
        """
        search_type_str: str = ",".join(search_type)
        params: dict[str, Any] = {
            "q": query,
            "type": search_type_str,
            "limit": limit,
        }

        if market is not None:
            params["market"] = market

        return self.make_request("/v1/search", params=params)

    def get_track(self, track_id: str) -> dict[str, Any]:
        """Retrieve information about a track.

        Args:
            track_id (str): Spotify track ID.

        Returns:
            Dict[str, Any]: JSON response containing track details.
        """
        return self.make_request(f"/v1/tracks/{track_id}")

    def get_artist(self, artist_id: str) -> dict[str, Any]:
        """Retrieve information about an artist.

        Args:
            artist_id (str): Spotify artist ID.

        Returns:
            Dict[str, Any]: JSON response containing artist details.
        """
        return self.make_request(f"/v1/artists/{artist_id}")

    def get_album(self, album_id: str) -> dict[str, Any]:
        """Retrieve information about an album.

        Args:
            album_id (str): Spotify album ID.

        Returns:
            Dict[str, Any]: JSON response containing album details.
        """
        return self.make_request(f"/v1/albums/{album_id}")
