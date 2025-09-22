import logging
import os
import sqlite3

logger = logging.getLogger(__name__)


def ensure_db(db_path: str, schema_path: str) -> None:
    os.makedirs(os.path.dirname(db_path), exist_ok=True)
    if not os.path.exists(db_path):
        logger.info("Database not found. Creating new DB at %s", db_path)
        with open(schema_path, encoding="utf-8") as f:
            schema_sql = f.read()
        with sqlite3.connect(db_path) as conn:
            conn.executescript(schema_sql)
        logger.info("Databe created with schema at %", schema_path)
    else:
        logger.info("Database already exists at %s", db_path)
