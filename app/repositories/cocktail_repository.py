from app.db import get_db

from app.repositories.cocktail_ingredient_repository import get_ingredients_for_cocktail


def get_all_cocktails():
    db = get_db()
    query = """
        SELECT id, name, country, region, preparation_time_minutes, cocktail_type_id, instructions, image_url, abv
        FROM cocktails
        ORDER BY name
    """
    rows = db.execute(query).fetchall()
    return [dict(r) for r in rows]


def search_cocktails(search_term):
    """Cerca i cocktail per nome o ingredienti usando LIKE."""
    db = get_db()
    search_pattern = f"%{search_term}%"
    query = """
        SELECT DISTINCT c.id, c.name, c.country, c.region, c.preparation_time_minutes, c.cocktail_type_id, c.instructions, c.image_url, c.abv
        FROM cocktails c
        LEFT JOIN cocktail_ingredients ci ON c.id = ci.cocktail_id
        LEFT JOIN ingredients i ON ci.ingredient_id = i.id
        WHERE c.name LIKE ? OR i.name LIKE ?
        ORDER BY c.name
    """
    rows = db.execute(query, (search_pattern, search_pattern)).fetchall()
    return [dict(r) for r in rows]


def get_cocktail_by_id(cocktail_id):
    db = get_db()
    query = """
        SELECT id, name, country, region, preparation_time_minutes, cocktail_type_id, instructions, image_url, abv
        FROM cocktails
        WHERE id = ?
    """
    row = db.execute(query, (cocktail_id,)).fetchone()
    if not row:
        return None
    cocktail = dict(row)
    # Aggiungi gli ingredienti
    cocktail['ingredients'] = get_ingredients_for_cocktail(cocktail_id)
    return cocktail


def create_cocktail(name, country, region, preparation_time_minutes, cocktail_type_id, instructions, image_url=None, ingredients=None):
    """Crea un cocktail e opzionalmente associa ingredienti.

    ingredients: lista di dict {ingredient_id, quantity, unit}
    """
    db = get_db()
    cursor = db.execute(
        "INSERT INTO cocktails (name, country, region, preparation_time_minutes, cocktail_type_id, instructions, image_url) VALUES (?, ?, ?, ?, ?, ?, ?)",
        (name, country, region, preparation_time_minutes, cocktail_type_id, instructions, image_url),
    )
    cocktail_id = cursor.lastrowid
    if ingredients:
        for ing in ingredients:
            db.execute(
                "INSERT INTO cocktail_ingredients (cocktail_id, ingredient_id, quantity, unit) VALUES (?, ?, ?, ?)",
                (cocktail_id, ing['ingredient_id'], ing['quantity'], ing.get('unit')),
            )
    db.commit()
    return cocktail_id


def update_cocktail(cocktail_id, name, country, region, preparation_time_minutes, cocktail_type_id, instructions, image_url=None, ingredients=None):
    db = get_db()
    db.execute(
        "UPDATE cocktails SET name = ?, country = ?, region = ?, preparation_time_minutes = ?, cocktail_type_id = ?, instructions = ?, image_url = ? WHERE id = ?",
        (name, country, region, preparation_time_minutes, cocktail_type_id, instructions, image_url, cocktail_id),
    )
    # Se viene passata la lista ingredients, rimpiazziamo le associazioni esistenti
    if ingredients is not None:
        db.execute("DELETE FROM cocktail_ingredients WHERE cocktail_id = ?", (cocktail_id,))
        for ing in ingredients:
            db.execute(
                "INSERT INTO cocktail_ingredients (cocktail_id, ingredient_id, quantity, unit) VALUES (?, ?, ?, ?)",
                (cocktail_id, ing['ingredient_id'], ing['quantity'], ing.get('unit')),
            )
    db.commit()


def delete_cocktail(cocktail_id):
    db = get_db()
    # ON DELETE CASCADE è definito per cocktail_ingredients, quindi basta cancellare il cocktail
    db.execute("DELETE FROM cocktails WHERE id = ?", (cocktail_id,))
    db.commit()
