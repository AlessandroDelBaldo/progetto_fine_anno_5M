from app.db import get_db


def get_all_cocktail_types():
    """
    Recupera tutti i tipi di cocktail.
    """
    db = get_db()
    query = """
        SELECT id, name, description
        FROM cocktail_types
        ORDER BY name
    """
    cocktail_types = db.execute(query).fetchall()
    return [dict(cocktail_type) for cocktail_type in cocktail_types]

def get_cocktail_type_by_id(cocktail_type_id):
    """Recupera un singolo tipo di cocktail per ID."""
    db = get_db()
    query = """
        SELECT id, name, description
        FROM cocktail_types
        WHERE id = ?
    """
    cocktail_type = db.execute(query, (cocktail_type_id,)).fetchone()
    if cocktail_type:
        return dict(cocktail_type)
    return None


def create_cocktail_type(name, description):
    """Crea un nuovo tipo di cocktail."""
    db = get_db()
    cursor = db.execute(
        "INSERT INTO cocktail_types (name, description) VALUES (?, ?)",
        (name, description),
    )
    db.commit()
    return cursor.lastrowid
