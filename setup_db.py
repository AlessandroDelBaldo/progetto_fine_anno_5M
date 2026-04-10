import os
import sqlite3
from app import create_app


def main():
    # Creiamo l'app per ottenere i percorsi di istanza/config
    app = create_app()

    # Assicuriamoci che la cartella instance esista
    instance_path = app.instance_path
    os.makedirs(instance_path, exist_ok=True)

    # Percorso al DB definito nella configurazione dell'app
    db_path = app.config.get('DATABASE')
    if not db_path:
        # fallback: file nella instance
        db_path = os.path.join(instance_path, 'recipes.sqlite')

    # Leggiamo lo schema dal file corretto
    schema_path = os.path.join(os.path.dirname(__file__), 'app', 'schema.sql')
    if not os.path.exists(schema_path):
        # percorso alternativo (se la struttura è diversa)
        schema_path = os.path.join(os.path.dirname(__file__), 'schema.sql')

    if not os.path.exists(schema_path):
        raise FileNotFoundError(f"schema.sql non trovato in percorsi previsti."
                                f" Controlla {schema_path} o app/schema.sql")

    # Applichiamo lo schema
    conn = sqlite3.connect(db_path)
    with open(schema_path, 'r', encoding='utf-8') as f:
        conn.executescript(f.read())
    conn.close()

    print("Database creato con successo in:", db_path)


if __name__ == '__main__':
    main()