import base64
import re
from typing import Any

import pytest

from api.spotify_api import SpotifyAPI


def test_init_raises_when_missing_env(monkeypatch: Any) -> None:
    # Deleting environmental variables
    monkeypatch.delenv("CLIENT_ID", raising=False)
    monkeypatch.delenv("CLIENT_SECRET", raising=False)

    with pytest.raises(
        ValueError,
        match=re.escape("Missing CLIENT_ID or CLIENT_SECRET in environment variables."),
    ):
        SpotifyAPI()


def test_init_builds_base64_correctly() -> None:
    client = SpotifyAPI()

    expected = base64.b64encode(b"dummy_id:dummy_secret").decode()
    assert client.client_creds_b64 == expected


def test_get_token_success(mocker: Any) -> None:
    client = SpotifyAPI()

    fake_response = mocker.Mock()
    fake_response.status_code = 200
    fake_response.json.return_value = {
        "access_token": "dummy_token",
        "expires_in": 3600,
    }

    mocker.patch("requests.post", return_value=fake_response)

    token = client.get_token()

    assert token == "dummy_token"  # noqa: S105
    assert client.access_token == "dummy_token"  # noqa: S105
    assert client.expires_in == 3600


def test_get_token_failure(mocker: Any) -> None:
    client = SpotifyAPI()

    fake_response = mocker.Mock()
    fake_response.status_code = 400
    fake_response.text = "dummy_text"

    mocker.patch("requests.post", return_value=fake_response)

    with pytest.raises(
        RuntimeError, match=re.escape("Failed to get token: 400 dummy_text")
    ):
        client.get_token()


def test_get_headers_without_token() -> None:
    client = SpotifyAPI()
    with pytest.raises(
        RuntimeError, match=re.escape("No access token. Call get_token() first.")
    ):
        client.get_headers()


def test_get_headers_with_token() -> None:
    client = SpotifyAPI()
    client.access_token = "dummy"  # noqa: S105

    headers = client.get_headers()
    assert headers["Authorization"] == "Bearer dummy"
    assert headers["Content-Type"] == "application/json"


def test_make_request_json_response(mocker: Any) -> None:
    client = SpotifyAPI()

    mocker.patch.object(
        client, "get_headers", return_value={"Authorizaiton": "Bearer dummy"}
    )

    fake_response = mocker.Mock()
    fake_response.status_code = 200
    fake_response.json.return_value = {"name": "Taylor Swift"}

    mocker.patch("requests.get", return_value=fake_response)

    result = client.make_request("/v1/tracks/123")

    assert result == {"name": "Taylor Swift"}


def test_make_request_failed(mocker: Any) -> None:
    client = SpotifyAPI()

    mocker.patch.object(
        client, "get_headers", return_value={"Authorization": "Bearer dummy"}
    )

    fake_response = mocker.Mock()
    fake_response.status_code = 400
    fake_response.text = "dummy_text"

    mocker.patch("requests.get", return_value=fake_response)

    with pytest.raises(
        RuntimeError, match=re.escape("Failed to make request: 400 dummy_text")
    ):
        client.make_request("/dummy_url")


def test_search(mocker: Any) -> None:
    client = SpotifyAPI()

    fake_result = {"tracks": {"items": ["dummy_tracks"]}}
    mock_make_request = mocker.patch.object(
        client, "make_request", return_value=fake_result
    )

    result = client.search("Taylor Swift", ["track", "album"], limit=5, market="US")

    mock_make_request.assert_called_once_with(
        "/v1/search",
        params={"q": "Taylor Swift", "type": "track,album", "limit": 5, "market": "US"},
    )

    assert result == fake_result
