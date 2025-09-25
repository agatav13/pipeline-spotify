from datetime import datetime
from pipeline.transform import TransformSpotify


def test_clean_album_valid_data():
    raw_album = {
        "id": "123",
        "name": "  Test Album  ",
        "album_type": "album",
        "artists": [
            {"id": "a1", "name": "Artist One", "external_urls": {"spotify": "url1"}},
            {"id": "a2", "name": "Artist Two"},
        ],
        "images": [
            {"url": "img_small", "width": 200},
            {"url": "img_large", "width": 1000},
        ],
        "total_tracks": "10",
        "release_date": "2024-05-10",
        "release_date_precision": "day",
        "external_urls": {"spotify": "album_url"},
        "extracted_at": "2025-09-25T10:00:00Z",
        "extraction_type": "new_releases"
    }

    transformer = TransformSpotify()
    cleaned = transformer.clean_album(raw_album=raw_album)

    assert cleaned["album_id"] == "123"
    assert cleaned["album_name"] == "Test Album"
    assert cleaned["album_type"] == "album"
    assert cleaned["artists"][0]["artist_name"] == "Artist One"
    assert cleaned["primary_artist_name"] == "Artist One"
    assert cleaned["primary_artist_id"] == "a1"
    assert cleaned["image_url"] == "img_large"
    assert cleaned["total_tracks"] == 10
    assert cleaned["release_year"] == 2024
    assert cleaned["spotify_url"] == "album_url"
    assert cleaned["extracted_at"] == "2025-09-25T10:00:00Z"
    assert cleaned["extraction_type"] == "new_releases"
    assert cleaned["data_type"] == "album"
    datetime.fromisoformat(cleaned["processed_at"])

def test_clean_album_missing_id_or_name_skips():
    transformer = TransformSpotify()
    assert transformer.clean_album({"name": "No ID"}) is None
    assert transformer.clean_album({"id": "123"}) is None

def test_clean_album_invalid_total_tracks_and_release_date():
    raw_album = {
        "id": "456",
        "name": "Album",
        "total_tracks": "not_a_number",
        "release_date": "invalid-date",
    }
    transformer = TransformSpotify()
    cleaned = transformer.clean_album(raw_album)

    assert cleaned["total_tracks"] is None
    assert cleaned["release_year"] is None

def test_clean_album_no_artists_or_images():
    raw_album = {
        "id": "789",
        "name": "No Artists or Images",
    }
    transformer = TransformSpotify()
    cleaned = transformer.clean_album(raw_album)

    assert cleaned["artists"] == []
    assert cleaned["primary_artist_name"] == "Unknown"
    assert cleaned["primary_artist_id"] is None
    assert cleaned["image_url"] is None

def test_transform_new_releases_filters_and_transforms():
    transformer = TransformSpotify()
    raw_albums = [
        {"id": "1", "name": "Valid Album"},
        {"name": "Missing ID"},  # invalid
    ]
    result = transformer.transform_new_releases(raw_albums)

    assert len(result) == 1
    assert result[0]["album_id"] == "1"