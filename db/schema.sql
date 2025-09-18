CREATE TABLE IF NOT EXISTS artist (
    artist_id TEXT PRIMARY KEY,
    artist_name TEXT NOT NULL,
    spotify_url TEXT,
    extracted_at TEXT,
    processed_at TEXT
);

CREATE TABLE IF NOT EXISTS album (
    album_id TEXT PRIMARY KEY,
    album_name TEXT NOT NULL,
    album_type TEXT,
    release_date TEXT,
    release_year INTEGER,
    release_date_precision TEXT,
    total_tracks INTEGER,
    image_url TEXT,
    spotify_url TEXT,
    extracted_at TEXT,
    extraction_type TEXT,
    processed_at TEXT,
    data_type TEXT
);

-- (album <-> artist)
CREATE TABLE IF NOT EXISTS album_artist (
    album_id TEXT NOT NULL,
    artist_id TEXT NOT NULL,
    PRIMARY KEY (album_id, artist_id),
    FOREIGN KEY (album_id) REFERENCES album(album_id) ON DELETE CASCADE,
    FOREIGN KEY (artist_id) REFERENCES artist(artist_id) ON DELETE CASCADE
);
