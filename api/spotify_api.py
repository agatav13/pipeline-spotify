"""Class for handling Spotify API."""
import base64
import os

import requests
from dotenv import load_dotenv

load_dotenv()


class SpotifyAPI:
    """Class for handling Spotify API."""
    TOKEN_URL: str = "https://accounts.spotify.com/api/token"

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


spotify_client = SpotifyAPI()
token = spotify_client.get_token()
print(token)
