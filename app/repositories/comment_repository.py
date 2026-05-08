from datetime import datetime
from app.db import get_db


def get_comments_for_cocktail(cocktail_id):
    db = get_db()
    rows = db.execute(
        """
        SELECT c.id, c.content, c.created_at, u.username
        FROM comments c
        JOIN users u ON u.id = c.user_id
        WHERE c.cocktail_id = ?
        ORDER BY c.created_at ASC
        """,
        (cocktail_id,),
    ).fetchall()
    return [dict(r) for r in rows]


def add_comment(cocktail_id, user_id, content):
    db = get_db()
    created_at = datetime.now().strftime('%d/%m/%Y %H:%M')
    cursor = db.execute(
        "INSERT INTO comments (cocktail_id, user_id, content, created_at) VALUES (?, ?, ?, ?)",
        (cocktail_id, user_id, content, created_at),
    )
    db.commit()
    return cursor.lastrowid


def delete_comment(comment_id, user_id):
    """Elimina un commento solo se appartiene all'utente."""
    db = get_db()
    db.execute(
        "DELETE FROM comments WHERE id = ? AND user_id = ?",
        (comment_id, user_id),
    )
    db.commit()
