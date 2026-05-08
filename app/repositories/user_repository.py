from app.db import get_db


def create_user(email, username, password_hash):
    db = get_db()
    cursor = db.execute(
        "INSERT INTO users (email, username, password_hash) VALUES (?, ?, ?)",
        (email, username, password_hash),
    )
    db.commit()
    return cursor.lastrowid


def get_user_by_username(username):
    db = get_db()
    row = db.execute("SELECT * FROM users WHERE username = ?", (username,)).fetchone()
    return dict(row) if row else None


def get_user_by_email(email):
    db = get_db()
    row = db.execute("SELECT * FROM users WHERE email = ?", (email,)).fetchone()
    return dict(row) if row else None


def get_user_by_id(user_id):
    db = get_db()
    row = db.execute("SELECT * FROM users WHERE id = ?", (user_id,)).fetchone()
    return dict(row) if row else None


def get_user_by_reset_token(token):
    db = get_db()
    row = db.execute("SELECT * FROM users WHERE reset_token = ?", (token,)).fetchone()
    return dict(row) if row else None


def set_reset_token(user_id, token, expires):
    db = get_db()
    db.execute(
        "UPDATE users SET reset_token = ?, reset_token_expires = ? WHERE id = ?",
        (token, expires, user_id),
    )
    db.commit()


def update_password(user_id, password_hash):
    db = get_db()
    db.execute(
        "UPDATE users SET password_hash = ? WHERE id = ?",
        (password_hash, user_id),
    )
    db.commit()


def clear_reset_token(user_id):
    db = get_db()
    db.execute(
        "UPDATE users SET reset_token = NULL, reset_token_expires = NULL WHERE id = ?",
        (user_id,),
    )
    db.commit()
