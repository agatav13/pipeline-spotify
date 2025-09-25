from datetime import datetime
import pytest

from pipeline.extract import ExtractSpotify

def test_init_calls_get_token(mocker):
    mock_client = mocker.patch("pipeline.extract.SpotifyAPI")
    mock_instance = mock_client.return_value

    extractor = ExtractSpotify()

    mock_instance.get_token.assert_called_once()
    assert extractor.client is mock_instance


def test_extract_new_releases_returns_albums(mocker):
    mock_client = mocker.patch("pipeline.extract.SpotifyAPI")
    mock_instance = mock_client.return_value
    mock_instance.get_new_releases.return_value = {
        "albums": {"items": [{"album_name": "Test Album"}]}
    }

    extractor = ExtractSpotify()
    result = extractor.extract_new_releases(limit=1)

    assert isinstance(result, list)
    assert len(result) == 1
    album = result[0]
    assert album["album_name"] == "Test Album"
    assert "extracted_at" in album
    assert album["extraction_type"] == "new_releases"

    datetime.fromisoformat(album["extracted_at"])

def test_extract_new_releases_raises_on_error(mocker):
    mock_client = mocker.patch("pipeline.extract.SpotifyAPI")
    mock_instance = mock_client.return_value
    mock_instance.get_new_releases.side_effect = Exception("API Error")

    extractor = ExtractSpotify()

    with pytest.raises(Exception, match="Failed to extract new releases."):
        extractor.extract_new_releases(limit=1)  
