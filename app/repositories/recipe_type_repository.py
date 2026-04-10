from app.db import get_db


def get_all_recipe_types():
    """
    Recupera tutti i tipi di ricetta.
    """
    db = get_db()
    query = """
        SELECT id, name, description
        FROM recipe_types
        ORDER BY name
    """
    recipe_types = db.execute(query).fetchall()
    return [dict(recipe_type) for recipe_type in recipe_types]

def get_recipe_type_by_id(recipe_type_id):
    """Recupera un singolo tipo di ricetta per ID."""
    db = get_db()
    query = """
        SELECT id, name, description
        FROM recipe_types
        WHERE id = ?
    """
    recipe_type = db.execute(query, (recipe_type_id,)).fetchone()
    if recipe_type:
        return dict(recipe_type)
    return None


def create_recipe_type(name, description):
    """Crea un nuovo tipo di ricetta."""
    db = get_db()
    cursor = db.execute(
        "INSERT INTO recipe_types (name, description) VALUES (?, ?)",
        (name, description),
    )
    db.commit()
    return cursor.lastrowid
