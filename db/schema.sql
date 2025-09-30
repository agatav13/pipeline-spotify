CREATE TABLE IF NOT EXISTS artist (
    artist_id TEXT PRIMARY KEY,
    artist_name TEXT NOT NULL,
    spotify_url TEXT,
    extracted_at TIMESTAMPTZ,
    processed_at TIMESTAMPTZ
);

CREATE TABLE IF NOT EXISTS album (
    album_id TEXT PRIMARY KEY,
    album_name TEXT NOT NULL,
    album_type TEXT,
    release_date DATE,
    release_year INTEGER,
    release_date_precision TEXT,
    total_tracks INTEGER,
    image_url TEXT,
    spotify_url TEXT,
    extracted_at TIMESTAMPTZ,
    extraction_type TEXT,
    processed_at TIMESTAMPTZ,
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

CREATE TABLE IF NOT EXISTS pipeline_metrics (
    id SERIAL PRIMARY KEY,
    run_at TIMESTAMP DEFAULT NOW(),   -- kiedy pipeline się wykonał
    operation TEXT NOT NULL,          -- np. "load_new_releases"
    status TEXT NOT NULL,             -- "success" albo "failure"
    rows_added INT,                   -- ile nowych wierszy (opcjonalnie)
    total_albums INT,                 -- ile albumów w bazie po runie
    total_artists INT,                -- ile artystów
    total_album_artist INT            -- ile powiązań album-artist
);
