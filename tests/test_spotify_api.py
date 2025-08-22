import pytest

from api.spotify_api import SpotifyAPI


def test_get_headers_without_token():
    client = SpotifyAPI()
    with pytest.raises(RuntimeError, match="No access token"):
        client.get_headers()


def test_get_headers_with_token():
    client = SpotifyAPI()
    client.access_token = "dummy"

    headers = client.get_headers()
    assert headers["Authorization"] == "Bearer dummy"
    assert headers["Content-Type"] == "application/json"
