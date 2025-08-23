import base64
import re
import pytest

from api.spotify_api import SpotifyAPI


def test_init_raises_when_missing_env(monkeypatch):
    # Deleting environmental variables
    monkeypatch.delenv("CLIENT_ID", raising=False)
    monkeypatch.delenv("CLIENT_SECRET", raising=False)

    with pytest.raises(
        ValueError,
        match=re.escape("Missing CLIENT_ID or CLIENT_SECRET in environment variables."),
    ):
        SpotifyAPI()


def test_init_builds_base64_correctly(monkeypatch):
    monkeypatch.setenv("CLIENT_ID", "dummy_id")
    monkeypatch.setenv("CLIENT_SECRET", "dummy_secret")

    client = SpotifyAPI()

    expected = base64.b64encode("dummy_id:dummy_secret".encode()).decode()
    assert client.client_creds_b64 == expected


def test_get_headers_without_token():
    client = SpotifyAPI()
    with pytest.raises(
        RuntimeError, match=re.escape("No access token. Call get_token() first.")
    ):
        client.get_headers()


def test_get_headers_with_token():
    client = SpotifyAPI()
    client.access_token = "dummy"

    headers = client.get_headers()
    assert headers["Authorization"] == "Bearer dummy"
    assert headers["Content-Type"] == "application/json"
