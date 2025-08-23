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


def test_init_builds_base64_correctly():
    client = SpotifyAPI()

    expected = base64.b64encode(b"dummy_id:dummy_secret").decode()
    assert client.client_creds_b64 == expected


def test_get_token_success(mocker):
    client = SpotifyAPI()

    fake_response = mocker.Mock()
    fake_response.status_code = 200
    fake_response.json.return_value = {
        "access_token": "dummy_token",
        "expires_in": 3600,
    }

    mocker.patch("requests.post", return_value=fake_response)

    token = client.get_token()

    assert token == "dummy_token"
    assert client.access_token == "dummy_token"
    assert client.expires_in == 3600


def test_get_token_failure(mocker):
    client = SpotifyAPI()

    fake_response = mocker.Mock()
    fake_response.status_code = 400
    fake_response.text = "dummy_text"

    mocker.patch("requests.post", return_value=fake_response)

    with pytest.raises(
        RuntimeError, match=re.escape("Failed to get token: 400 dummy_text")
    ):
        client.get_token()


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
