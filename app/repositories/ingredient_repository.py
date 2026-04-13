from app.db import get_db


def get_all_ingredients():
    """
    Recupera tutti gli ingredienti.
    """
    db = get_db()
    query = """
        SELECT id, name, default_unit, image_url
        FROM ingredients
        ORDER BY name
    """
    rows = db.execute(query).fetchall()
    return [dict(row) for row in rows]


def get_ingredient_by_id(ingredient_id):
    db = get_db()
    query = """
        SELECT id, name, default_unit
        FROM ingredients
        WHERE id = ?
    """
    row = db.execute(query, (ingredient_id,)).fetchone()
    return dict(row) if row else None


def create_ingredient(name, default_unit):
    db = get_db()
    cursor = db.execute(
        "INSERT INTO ingredients (name, default_unit) VALUES (?, ?)",
        (name, default_unit),
    )
    db.commit()
    return cursor.lastrowid


def update_ingredient(ingredient_id, name, default_unit):
    db = get_db()
    db.execute(
        "UPDATE ingredients SET name = ?, default_unit = ? WHERE id = ?",
        (name, default_unit, ingredient_id),
    )
    db.commit()


def delete_ingredient(ingredient_id):
    db = get_db()
    db.execute("DELETE FROM ingredients WHERE id = ?", (ingredient_id,))
    db.commit()
