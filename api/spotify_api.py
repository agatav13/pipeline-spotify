"""Class for handling Spotify API."""

import base64
import os
from typing import Any

import requests
from dotenv import load_dotenv

load_dotenv()


class SpotifyAPI:
    """Class for handling Spotify API."""

    TOKEN_URL: str = "https://accounts.spotify.com/api/token"
    BASE_URL: str = "https://api.spotify.com"

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
        url = self.BASE_URL + endpoint
        headers = self.get_headers()

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
    ) -> dict[str, None]:
        search_type = ",".join(search_type)
        params = {
            "q": query,
            "type": search_type,
            "limit": limit,
        }

        if market is not None:
            params["market"] = market

        return self.make_request("/v1/search", params=params)

    def get_track(self, track_id: str):
        return self.make_request(f"/v1/tracks/{track_id}")

    def get_artist(self, artist_id: str):
        return self.make_request(f"/v1/artists/{artist_id}")

    def get_album(self, album_id: str):
        return self.make_request(f"/v1/albums/{album_id}")
