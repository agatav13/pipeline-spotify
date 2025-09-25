import logging
import os
from datetime import UTC, datetime

from dotenv import load_dotenv

from pipeline.pipeline import Pipeline

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")

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
    Pipeline(database_url=DATABASE_URL).run()
    logger.info("ETL pipeline finished successfully.")


if __name__ == "__main__":
    main()
