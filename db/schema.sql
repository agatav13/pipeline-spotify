CREATE TABLE IF NOT EXISTS artists (
    artist_id TEXT PRIMARY KEY,
    name TEXT NOT NULL,
    spotify_url TEXT,
    extracted_at TEXT,
    processed_at TEXT,
);

-- Albums table
CREATE TABLE IF NOT EXISTS albums (
    album_id TEXT PRIMARY KEY,
    name TEXT NOT NULL,
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
    data_type TEXT,
);

-- (albums <-> artists)
CREATE TABLE IF NOT EXISTS album_artists (
    album_id TEXT NOT NULL,
    artist_id TEXT NOT NULL,
    PRIMARY KEY (album_id, artist_id),
    FOREIGN KEY (album_id) REFERENCES albums(album_id) ON DELETE CASCADE,
    FOREIGN KEY (artist_id) REFERENCES artists(artist_id) ON DELETE CASCADE
);
