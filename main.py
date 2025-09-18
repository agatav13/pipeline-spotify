from db.setup_db import ensure_db
from pipeline.pipeline import Pipeline

DB_PATH = "db/spotify.db"
SCHEMA_PATH = "db/schema.sql"


def main():
    ensure_db(db_path=DB_PATH, schema_path=SCHEMA_PATH)
    Pipeline(db_path=DB_PATH).run()


if __name__ == "__main__":
    main()
