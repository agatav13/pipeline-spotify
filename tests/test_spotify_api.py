"""Unit tests for the SpotifyAPI class.

Covering authentication, requests, and resource retrieval.
"""

import base64
import re

import pytest

from api.spotify_api import SpotifyAPI


def test_init_raises_when_missing_env(monkeypatch):
    """Test error when required environment variables are missing.

    Ensures SpotifyAPI raises ValueError if CLIENT_ID or CLIENT_SECRET are not set.

    Args:
        monkeypatch: pytest fixture to modify environment variables.

    Raises:
        ValueError: If CLIENT_ID or CLIENT_SECRET are missing.
    """
    # Deleting environmental variables
    monkeypatch.delenv("CLIENT_ID", raising=False)
    monkeypatch.delenv("CLIENT_SECRET", raising=False)

    with pytest.raises(
        ValueError,
        match=re.escape("Missing CLIENT_ID or CLIENT_SECRET in environment variables."),
    ):
        SpotifyAPI()


def test_init_builds_base64_correctly():
    """Test that SpotifyAPI correctly builds the base64-encoded credentials.

    Asserts:
        The base64-encoded credentials match the expected value.
    """
    client = SpotifyAPI()

    expected = base64.b64encode(b"dummy_id:dummy_secret").decode()
    assert client.client_creds_b64 == expected


def test_get_token_success(mocker):
    """Test successful retrieval of access token from Spotify API.

    Args:
        mocker: pytest-mock fixture to mock requests.

    Asserts:
        The returned token, access_token, and expires_in are set correctly.
    """
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


def test_get_token_failure(mocker):
    """Test that SpotifyAPI raises RuntimeError when token retrieval fails.

    Args:
        mocker: pytest-mock fixture to mock requests.

    Raises:
        RuntimeError: If the token request fails.
    """
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
    """Test that get_headers raises RuntimeError if access token is missing.

    Raises:
        RuntimeError: If access token is not set.
    """
    client = SpotifyAPI()
    with pytest.raises(
        RuntimeError, match=re.escape("No access token. Call get_token() first.")
    ):
        client.get_headers()


def test_get_headers_with_token():
    """Test that get_headers returns correct headers when access token is set.

    Asserts:
        The Authorization and Content-Type headers are correct.
    """
    client = SpotifyAPI()
    client.access_token = "dummy"  # noqa: S105

    headers = client.get_headers()
    assert headers["Authorization"] == "Bearer dummy"
    assert headers["Content-Type"] == "application/json"


def test_make_request_json_response(mocker):
    """Test that make_request returns JSON response for successful GET request.

    Args:
        mocker: pytest-mock fixture to mock requests.

    Asserts:
        The returned result matches the expected JSON.
    """
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


def test_make_request_failed(mocker):
    """Test that make_request raises RuntimeError for failed GET request.

    Args:
        mocker: pytest-mock fixture to mock requests.

    Raises:
        RuntimeError: If the GET request fails.
    """
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


def test_search(mocker):
    """Test the search method for correct parameter passing and result.

    Args:
        mocker: pytest-mock fixture to mock make_request.

    Asserts:
        make_request is called with correct parameters and result matches expected.
    """
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


def test_get_track(mocker):
    """Test the get_track method for correct endpoint and result.

    Args:
        mocker: pytest-mock fixture to mock make_request.

    Asserts:
        make_request is called with correct endpoint and result matches expected.
    """
    client = SpotifyAPI()

    fake_result = {"id": "track123"}
    mock_make_request = mocker.patch.object(
        client, "make_request", return_value=fake_result
    )

    result = client.get_track("track123")

    mock_make_request.assert_called_once_with("/v1/tracks/track123")
    assert result == fake_result


def test_get_artist(mocker):
    """Test the get_artist method for correct endpoint and result.

    Args:
        mocker: pytest-mock fixture to mock make_request.

    Asserts:
        make_request is called with correct endpoint and result matches expected.
    """
    client = SpotifyAPI()

    fake_result = {"id": "artist123"}
    mock_make_request = mocker.patch.object(
        client, "make_request", return_value=fake_result
    )

    result = client.get_artist("artist123")

    mock_make_request.assert_called_once_with("/v1/artists/artist123")
    assert result == fake_result


def test_get_album(mocker):
    """Test the get_album method for correct endpoint and result.

    Args:
        mocker: pytest-mock fixture to mock make_request.

    Asserts:
        make_request is called with correct endpoint and result matches expected.
    """
    client = SpotifyAPI()

    fake_result = {"id": "album123"}
    mock_make_result = mocker.patch.object(
        client, "make_request", return_value=fake_result
    )

    result = client.get_album("album123")

    mock_make_result.assert_called_once_with("/v1/albums/album123")
    assert result == fake_result
