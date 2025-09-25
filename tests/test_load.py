import pytest
from unittest.mock import patch, MagicMock
from pipeline.load import LoadSpotify

@pytest.fixture
def sample_clean_album():
    return {
        "album_id": "1",
        "album_name": "Test Album",
        "album_type": "album",
        "release_date": "2024-01-01",
        "release_year": 2024,
        "release_date_precision": "day",
        "total_tracks": 10,
        "image_url": "img_url",
        "spotify_url": "album_url",
        "extracted_at": "2025-09-25T10:00:00Z",
        "extraction_type": "new_releases",
        "processed_at": "2025-09-25T11:00:00Z",
        "data_type": "album",
        "artists": [
            {"artist_id": "a1", "artist_name": "Artist One", "spotify_url": "a_url"}
        ],
    }

def test_load_album_executes_queries(sample_clean_album):
    loader = LoadSpotify(database_url="postgres://test")

    with patch("pipeline.load.psycopg2.connect") as mock_connect:
        mock_conn = MagicMock()
        mock_cursor = MagicMock()
        mock_connect.return_value.__enter__.return_value = mock_conn
        mock_conn.cursor.return_value.__enter__.return_value = mock_cursor

        loader.load_album(sample_clean_album)

        executed_queries = [call[0][0] for call in mock_cursor.execute.call_args_list]
        assert any("INSERT INTO album" in q for q in executed_queries)
        assert any("INSERT INTO artist" in q for q in executed_queries)
        assert any("INSERT INTO album_artist" in q for q in executed_queries)

        params = [call[0][1] for call in mock_cursor.execute.call_args_list]
        assert any("1" in p for p in params)

def test_load_new_releases_calls_load_album(mocker, sample_clean_album):
    loader = LoadSpotify(database_url="postgres://test")
    mock_load_album = mocker.patch.object(loader, "load_album")

    loader.load_new_releases([sample_clean_album, sample_clean_album])
    assert mock_load_album.call_count == 2
