import os
import sqlite3


def ensure_db(db_path: str, schema_path: str) -> None:
    os.makedirs(os.path.dirname(db_path), exist_ok=True)
    if not os.path.exists(db_path):
        with open(schema_path, encoding="utf-8") as f:
            schema_sql = f.read()
        with sqlite3.connect(db_path) as conn:
            conn.executescript(schema_sql)
