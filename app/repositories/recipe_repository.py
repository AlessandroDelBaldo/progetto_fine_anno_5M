from app.db import get_db

from app.repositories.recipe_ingredient_repository import get_ingredients_for_recipe


def get_all_recipes():
    db = get_db()
    query = """
        SELECT id, name, country, region, preparation_time_minutes, recipe_type_id, instructions
        FROM recipes
        ORDER BY name
    """
    rows = db.execute(query).fetchall()
    return [dict(r) for r in rows]


def get_recipe_by_id(recipe_id):
    db = get_db()
    query = """
        SELECT id, name, country, region, preparation_time_minutes, recipe_type_id, instructions
        FROM recipes
        WHERE id = ?
    """
    row = db.execute(query, (recipe_id,)).fetchone()
    if not row:
        return None
    recipe = dict(row)
    # Aggiungi gli ingredienti
    recipe['ingredients'] = get_ingredients_for_recipe(recipe_id)
    return recipe


def create_recipe(name, country, region, preparation_time_minutes, recipe_type_id, instructions, ingredients=None):
    """Crea una ricetta e opzionalmente associa ingredienti.

    ingredients: lista di dict {ingredient_id, quantity, unit}
    """
    db = get_db()
    cursor = db.execute(
        "INSERT INTO recipes (name, country, region, preparation_time_minutes, recipe_type_id, instructions) VALUES (?, ?, ?, ?, ?, ?)",
        (name, country, region, preparation_time_minutes, recipe_type_id, instructions),
    )
    recipe_id = cursor.lastrowid
    if ingredients:
        for ing in ingredients:
            db.execute(
                "INSERT INTO recipe_ingredients (recipe_id, ingredient_id, quantity, unit) VALUES (?, ?, ?, ?)",
                (recipe_id, ing['ingredient_id'], ing['quantity'], ing.get('unit')),
            )
    db.commit()
    return recipe_id


def update_recipe(recipe_id, name, country, region, preparation_time_minutes, recipe_type_id, instructions, ingredients=None):
    db = get_db()
    db.execute(
        "UPDATE recipes SET name = ?, country = ?, region = ?, preparation_time_minutes = ?, recipe_type_id = ?, instructions = ? WHERE id = ?",
        (name, country, region, preparation_time_minutes, recipe_type_id, instructions, recipe_id),
    )
    # Se viene passata la lista ingredients, rimpiazziamo le associazioni esistenti
    if ingredients is not None:
        db.execute("DELETE FROM recipe_ingredients WHERE recipe_id = ?", (recipe_id,))
        for ing in ingredients:
            db.execute(
                "INSERT INTO recipe_ingredients (recipe_id, ingredient_id, quantity, unit) VALUES (?, ?, ?, ?)",
                (recipe_id, ing['ingredient_id'], ing['quantity'], ing.get('unit')),
            )
    db.commit()


def delete_recipe(recipe_id):
    db = get_db()
    # ON DELETE CASCADE è definito per recipe_ingredients, quindi basta cancellare la ricetta
    db.execute("DELETE FROM recipes WHERE id = ?", (recipe_id,))
    db.commit()
