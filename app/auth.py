import secrets
import smtplib
import time
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from functools import wraps

from flask import (Blueprint, current_app, flash, redirect, render_template,
                   request, session, url_for)
from werkzeug.security import check_password_hash, generate_password_hash

from app.repositories import user_repository

bp = Blueprint('auth', __name__, url_prefix='/auth')


def login_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        if 'user_id' not in session:
            flash('Devi fare il login per vedere i dettagli del cocktail.', 'warning')
            return redirect(url_for('auth.login', next=request.url))
        return f(*args, **kwargs)
    return decorated


@bp.route('/login', methods=('GET', 'POST'))
def login():
    if session.get('user_id'):
        return redirect(url_for('main.index'))

    if request.method == 'POST':
        email = request.form.get('email', '').strip().lower()
        password = request.form.get('password', '')
        next_url = request.form.get('next', '').strip()

        user = user_repository.get_user_by_email(email)
        if not user or not check_password_hash(user['password_hash'], password):
            flash('Email o password errati.', 'error')
        else:
            session.clear()
            session['user_id'] = user['id']
            return redirect(next_url or url_for('main.index'))

    return render_template('auth/login.html', next=request.args.get('next', ''))


@bp.route('/register', methods=('GET', 'POST'))
def register():
    if session.get('user_id'):
        return redirect(url_for('main.index'))

    if request.method == 'POST':
        email = request.form.get('email', '').strip().lower()
        username = request.form.get('username', '').strip()
        password = request.form.get('password', '')
        confirm = request.form.get('confirm_password', '')

        error = None
        if not email or '@' not in email:
            error = 'Email non valida.'
        elif not username:
            error = 'Il nome utente è obbligatorio.'
        elif len(password) < 8:
            error = 'La password deve essere di almeno 8 caratteri.'
        elif password != confirm:
            error = 'Le password non coincidono.'
        elif user_repository.get_user_by_email(email):
            error = 'Email già registrata.'
        elif user_repository.get_user_by_username(username):
            error = 'Nome utente già in uso.'

        if error:
            flash(error, 'error')
        else:
            user_repository.create_user(email, username, generate_password_hash(password))
            flash('Registrazione completata! Ora puoi fare il login.', 'success')
            return redirect(url_for('auth.login'))

    return render_template('auth/register.html')


@bp.route('/logout')
def logout():
    session.clear()
    flash('Hai effettuato il logout.', 'success')
    return redirect(url_for('main.index'))


@bp.route('/forgot-password', methods=('GET', 'POST'))
def forgot_password():
    if request.method == 'POST':
        email = request.form.get('email', '').strip().lower()
        user = user_repository.get_user_by_email(email)

        if user:
            token = secrets.token_urlsafe(32)
            expires = time.time() + 3600
            user_repository.set_reset_token(user['id'], token, expires)
            reset_url = url_for('auth.reset_password', token=token, _external=True)
            try:
                _send_reset_email(email, reset_url)
            except Exception as e:
                current_app.logger.error('Email reset fallita per %s: %s', email, e)

        flash("Se l'email è registrata, riceverai un link per il reset della password.", 'success')
        return redirect(url_for('auth.login'))

    return render_template('auth/forgot_password.html')


@bp.route('/reset-password/<token>', methods=('GET', 'POST'))
def reset_password(token):
    user = user_repository.get_user_by_reset_token(token)

    if not user or not user.get('reset_token_expires') or time.time() > user['reset_token_expires']:
        flash('Link di reset non valido o scaduto.', 'error')
        return redirect(url_for('auth.forgot_password'))

    if request.method == 'POST':
        password = request.form.get('password', '')
        confirm = request.form.get('confirm_password', '')

        if len(password) < 8:
            flash('La password deve essere di almeno 8 caratteri.', 'error')
        elif password != confirm:
            flash('Le password non coincidono.', 'error')
        else:
            user_repository.update_password(user['id'], generate_password_hash(password))
            user_repository.clear_reset_token(user['id'])
            flash('Password aggiornata! Ora puoi fare il login.', 'success')
            return redirect(url_for('auth.login'))

    return render_template('auth/reset_password.html', token=token)


def _send_reset_email(to_email, reset_url):
    host = current_app.config['MAIL_SMTP_HOST']
    port = int(current_app.config['MAIL_SMTP_PORT'])
    user = current_app.config['MAIL_SMTP_USER']
    password = current_app.config['MAIL_SMTP_PASS']
    sender = current_app.config['MAIL_SENDER'] or user

    msg = MIMEMultipart()
    msg['From'] = sender
    msg['To'] = to_email
    msg['Subject'] = 'Reset password – App Cocktail'
    msg.attach(MIMEText(
        f"Hai richiesto il reset della password per App Cocktail.\n\n"
        f"Clicca sul link seguente per reimpostare la tua password (valido 1 ora):\n"
        f"{reset_url}\n\n"
        f"Se non hai richiesto il reset, ignora questa email.",
        'plain'
    ))

    with smtplib.SMTP(host, port) as server:
        server.starttls()
        server.login(user, password)
        server.send_message(msg)
