import sys
import os
import sqlite3
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from app import create_app


def main():
    app = create_app()

    instance_path = app.instance_path
    os.makedirs(instance_path, exist_ok=True)

    db_path = app.config.get('DATABASE') or os.path.join(instance_path, 'cocktails.sqlite')
    schema_path = Path(__file__).resolve().parents[1] / 'app' / 'schema.sql'

    if not schema_path.exists():
        raise FileNotFoundError(f"schema.sql non trovato: {schema_path}")

    conn = sqlite3.connect(str(db_path))
    with open(schema_path, 'r', encoding='utf-8') as f:
        conn.executescript(f.read())
    conn.close()

    print("Database creato con successo in:", db_path)


if __name__ == '__main__':
    main()
