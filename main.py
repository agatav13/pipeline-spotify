import logging
import os
from datetime import UTC, datetime

from db.setup_db import ensure_db
from pipeline.pipeline import Pipeline

DB_PATH = "db/spotify.db"
SCHEMA_PATH = "db/schema.sql"

os.makedirs("logs", exist_ok=True)

log_filename = f"logs/etl_{datetime.now(UTC).strftime('%Y-%m-%d')}.log"
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
    handlers=[
        logging.FileHandler(log_filename, encoding="utf-8"),
        logging.StreamHandler(),
    ],
)
logger = logging.getLogger(__name__)


def main():
    logger.info("Starting ETL pipeline...")
    ensure_db(db_path=DB_PATH, schema_path=SCHEMA_PATH)
    Pipeline(db_path=DB_PATH).run()
    logger.info("ETL pipeline finished successfully.")


if __name__ == "__main__":
    main()
