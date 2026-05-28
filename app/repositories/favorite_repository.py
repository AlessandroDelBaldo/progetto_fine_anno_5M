from app.db import get_db


def get_favorite_ids(user_id):
    """Restituisce il set degli id cocktail nei preferiti dell'utente."""
    db = get_db()
    rows = db.execute(
        "SELECT cocktail_id FROM favorites WHERE user_id = ?",
        (user_id,),
    ).fetchall()
    return {r['cocktail_id'] for r in rows}


def is_favorite(user_id, cocktail_id):
    db = get_db()
    row = db.execute(
        "SELECT 1 FROM favorites WHERE user_id = ? AND cocktail_id = ?",
        (user_id, cocktail_id),
    ).fetchone()
    return row is not None


def get_favorite_cocktails(user_id):
    """Restituisce i cocktail preferiti dell'utente con tutti i campi."""
    db = get_db()
    rows = db.execute(
        """
        SELECT c.id, c.name, c.country, c.region, c.preparation_time_minutes,
               c.cocktail_type_id, c.instructions, c.image_url, c.abv
        FROM favorites f
        JOIN cocktails c ON c.id = f.cocktail_id
        WHERE f.user_id = ?
        ORDER BY c.name
        """,
        (user_id,),
    ).fetchall()
    return [dict(r) for r in rows]


def toggle_favorite(user_id, cocktail_id):
    """Aggiunge o rimuove dai preferiti. Ritorna True se ora è preferito."""
    db = get_db()
    existing = db.execute(
        "SELECT 1 FROM favorites WHERE user_id = ? AND cocktail_id = ?",
        (user_id, cocktail_id),
    ).fetchone()
    if existing:
        db.execute(
            "DELETE FROM favorites WHERE user_id = ? AND cocktail_id = ?",
            (user_id, cocktail_id),
        )
        db.commit()
        return False
    else:
        db.execute(
            "INSERT INTO favorites (user_id, cocktail_id) VALUES (?, ?)",
            (user_id, cocktail_id),
        )
        db.commit()
        return True
