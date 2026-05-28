from flask import Blueprint, flash, redirect, render_template, request, session, url_for
from werkzeug.exceptions import abort

from app.auth import login_required
from app.repositories import (cocktail_repository, cocktail_type_repository,
                               comment_repository, favorite_repository,
                               ingredient_repository)

bp = Blueprint("main", __name__)


def _enrich_with_types(cocktails):
    types = {t['id']: t['name'] for t in cocktail_type_repository.get_all_cocktail_types()}
    for c in cocktails:
        c['type_name'] = types.get(c.get('cocktail_type_id'))


@bp.route("/")
def index():
    cocktails = cocktail_repository.get_all_cocktails()
    _enrich_with_types(cocktails)
    return render_template('home.html', cocktails=cocktails, search_query=None)


@bp.route('/search')
def search_page():
    search_query = request.args.get('q', '').strip()
    cocktails = (cocktail_repository.search_cocktails(search_query)
                 if search_query
                 else cocktail_repository.get_all_cocktails())
    _enrich_with_types(cocktails)
    return render_template('home.html', cocktails=cocktails, search_query=search_query)


@bp.route('/cocktails')
def search_cocktails():
    cocktails = cocktail_repository.get_all_cocktails()
    _enrich_with_types(cocktails)
    return render_template('cocktails_list.html', cocktails=cocktails)


@bp.route('/cocktails/<int:id>')
@login_required
def cocktail_detail(id):
    cocktail = cocktail_repository.get_cocktail_by_id(id)
    if cocktail is None:
        abort(404, "Cocktail non trovato.")

    type_obj = None
    if cocktail.get('cocktail_type_id'):
        for t in cocktail_type_repository.get_all_cocktail_types():
            if t['id'] == cocktail['cocktail_type_id']:
                type_obj = t
                break

    comments = comment_repository.get_comments_for_cocktail(id)
    is_fav = favorite_repository.is_favorite(session['user_id'], id)

    return render_template('cocktail_detail.html',
                           cocktail=cocktail, type=type_obj,
                           comments=comments, is_fav=is_fav)


@bp.route('/cocktails/create', methods=('GET', 'POST'))
@login_required
def create_cocktail():
    types = cocktail_type_repository.get_all_cocktail_types()
    ingredients = ingredient_repository.get_all_ingredients()

    if request.method == 'POST':
        name = request.form.get('name')
        if not name:
            flash('Il nome è obbligatorio.', 'error')
        else:
            cocktail_repository.create_cocktail(
                name,
                request.form.get('country'),
                request.form.get('region'),
                request.form.get('preparation_time_minutes', type=int),
                request.form.get('cocktail_type_id', type=int),
                request.form.get('instructions'),
                image_url=request.form.get('image_url'),
                ingredients=_parse_ingredient_form(),
            )
            flash('Cocktail creato con successo.', 'success')
            return redirect(url_for('main.search_cocktails'))

    return render_template('create_cocktail.html', types=types, ingredients=ingredients)


@bp.route('/cocktails/<int:id>/edit', methods=('GET', 'POST'))
@login_required
def edit_cocktail(id):
    cocktail = cocktail_repository.get_cocktail_by_id(id)
    if cocktail is None:
        abort(404, "Cocktail non trovato.")

    types = cocktail_type_repository.get_all_cocktail_types()
    ingredients = ingredient_repository.get_all_ingredients()

    if request.method == 'POST':
        name = request.form.get('name')
        if not name:
            flash('Il nome è obbligatorio.', 'error')
        else:
            cocktail_repository.update_cocktail(
                id, name,
                request.form.get('country'),
                request.form.get('region'),
                request.form.get('preparation_time_minutes', type=int),
                request.form.get('cocktail_type_id', type=int),
                request.form.get('instructions'),
                image_url=request.form.get('image_url'),
                ingredients=_parse_ingredient_form(),
            )
            flash('Cocktail aggiornato con successo.', 'success')
            return redirect(url_for('main.cocktail_detail', id=id))

    return render_template('edit_cocktail.html', cocktail=cocktail, types=types, ingredients=ingredients)


@bp.route('/cocktails/<int:id>/delete', methods=('POST',))
@login_required
def delete_cocktail(id):
    cocktail = cocktail_repository.get_cocktail_by_id(id)
    if cocktail is None:
        abort(404, "Cocktail non trovato.")
    cocktail_repository.delete_cocktail(id)
    flash(f'"{cocktail["name"]}" eliminato.', 'success')
    return redirect(url_for('main.search_cocktails'))


@bp.route('/cocktails/<int:id>/comment', methods=('POST',))
@login_required
def add_comment(id):
    content = request.form.get('content', '').strip()
    if not content:
        flash('Il commento non può essere vuoto.', 'error')
    else:
        comment_repository.add_comment(id, session['user_id'], content)
    return redirect(url_for('main.cocktail_detail', id=id))


@bp.route('/cocktails/<int:id>/comment/<int:comment_id>/delete', methods=('POST',))
@login_required
def delete_comment(id, comment_id):
    comment_repository.delete_comment(comment_id, session['user_id'])
    return redirect(url_for('main.cocktail_detail', id=id))


@bp.route('/cocktails/<int:id>/favorite', methods=('POST',))
@login_required
def toggle_favorite(id):
    favorite_repository.toggle_favorite(session['user_id'], id)
    next_url = request.form.get('next') or request.referrer or url_for('main.search_cocktails')
    return redirect(next_url)


@bp.route('/preferiti')
@login_required
def favorites():
    cocktails = favorite_repository.get_favorite_cocktails(session['user_id'])
    _enrich_with_types(cocktails)
    return render_template('favorites.html', cocktails=cocktails)


def _parse_ingredient_form():
    ing_list = []
    for iid, q, u in zip(
        request.form.getlist('ingredient_id'),
        request.form.getlist('quantity'),
        request.form.getlist('unit'),
    ):
        try:
            ing_list.append({'ingredient_id': int(iid), 'quantity': float(q), 'unit': u or None})
        except (ValueError, TypeError):
            continue
    return ing_list
