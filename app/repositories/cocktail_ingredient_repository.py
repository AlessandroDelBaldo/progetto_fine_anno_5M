from app.db import get_db


def get_ingredients_for_cocktail(cocktail_id):
    """Restituisce gli ingredienti associati a un cocktail con quantità e unità."""
    db = get_db()
    query = """
        SELECT i.id AS ingredient_id, i.name AS ingredient_name, i.default_unit, i.image_url,
               ci.quantity, ci.unit
        FROM cocktail_ingredients ci
        JOIN ingredients i ON i.id = ci.ingredient_id
        WHERE ci.cocktail_id = ?
        ORDER BY i.name
    """
    rows = db.execute(query, (cocktail_id,)).fetchall()
    return [dict(r) for r in rows]


def add_ingredient_to_cocktail(cocktail_id, ingredient_id, quantity, unit=None):
    db = get_db()
    db.execute(
        "INSERT OR REPLACE INTO cocktail_ingredients (cocktail_id, ingredient_id, quantity, unit) VALUES (?, ?, ?, ?)",
        (cocktail_id, ingredient_id, quantity, unit),
    )
    db.commit()


def update_cocktail_ingredient(cocktail_id, ingredient_id, quantity, unit=None):
    db = get_db()
    db.execute(
        "UPDATE cocktail_ingredients SET quantity = ?, unit = ? WHERE cocktail_id = ? AND ingredient_id = ?",
        (quantity, unit, cocktail_id, ingredient_id),
    )
    db.commit()


def delete_cocktail_ingredient(cocktail_id, ingredient_id):
    db = get_db()
    db.execute(
        "DELETE FROM cocktail_ingredients WHERE cocktail_id = ? AND ingredient_id = ?",
        (cocktail_id, ingredient_id),
    )
    db.commit()
