from app.db import get_db


def get_ingredients_for_recipe(recipe_id):
    """Restituisce gli ingredienti associati a una ricetta con quantità e unità."""
    db = get_db()
    query = """
        SELECT i.id AS ingredient_id, i.name AS ingredient_name, i.default_unit,
               ri.quantity, ri.unit
        FROM recipe_ingredients ri
        JOIN ingredients i ON i.id = ri.ingredient_id
        WHERE ri.recipe_id = ?
        ORDER BY i.name
    """
    rows = db.execute(query, (recipe_id,)).fetchall()
    return [dict(r) for r in rows]


def add_ingredient_to_recipe(recipe_id, ingredient_id, quantity, unit=None):
    db = get_db()
    db.execute(
        "INSERT OR REPLACE INTO recipe_ingredients (recipe_id, ingredient_id, quantity, unit) VALUES (?, ?, ?, ?)",
        (recipe_id, ingredient_id, quantity, unit),
    )
    db.commit()


def update_recipe_ingredient(recipe_id, ingredient_id, quantity, unit=None):
    db = get_db()
    db.execute(
        "UPDATE recipe_ingredients SET quantity = ?, unit = ? WHERE recipe_id = ? AND ingredient_id = ?",
        (quantity, unit, recipe_id, ingredient_id),
    )
    db.commit()


def delete_recipe_ingredient(recipe_id, ingredient_id):
    db = get_db()
    db.execute(
        "DELETE FROM recipe_ingredients WHERE recipe_id = ? AND ingredient_id = ?",
        (recipe_id, ingredient_id),
    )
    db.commit()
