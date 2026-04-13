from flask import Blueprint, flash, redirect, render_template, request, url_for
from app.repositories import cocktail_repository, ingredient_repository, cocktail_type_repository

# Usiamo 'main' perché è il blueprint principale del sito
bp = Blueprint("main", __name__)


@bp.route("/")
def index():
    # Mostra direttamente la lista dei cocktail (landing principale)
    cocktails = cocktail_repository.get_all_cocktails()
    types = {t['id']: t['name'] for t in cocktail_type_repository.get_all_cocktail_types()}
    for c in cocktails:
        c['type_name'] = types.get(c.get('cocktail_type_id'))
    return render_template('home.html', cocktails=cocktails, search_query=None)


@bp.route('/search')
def search_page():
    """Pagina di ricerca dei cocktail."""
    search_query = request.args.get('q', '').strip()
    
    if search_query:
        cocktails = cocktail_repository.search_cocktails(search_query)
    else:
        cocktails = cocktail_repository.get_all_cocktails()
    
    # Arricchisci con tipo di cocktail (nome)
    types = {t['id']: t['name'] for t in cocktail_type_repository.get_all_cocktail_types()}
    for c in cocktails:
        c['type_name'] = types.get(c.get('cocktail_type_id'))
    
    return render_template('home.html', cocktails=cocktails, search_query=search_query)


@bp.route('/cocktails')
def search_cocktails():
    """Lista tutti i cocktail disponibili."""
    cocktails = cocktail_repository.get_all_cocktails()
    # arricchisci con tipo di cocktail (nome)
    types = {t['id']: t['name'] for t in cocktail_type_repository.get_all_cocktail_types()}
    for c in cocktails:
        c['type_name'] = types.get(c.get('cocktail_type_id'))
    return render_template('cocktails_list.html', cocktails=cocktails)


@bp.route('/cocktails/<int:id>')
def cocktail_detail(id):
    """Mostra i dettagli di un singolo cocktail."""
    cocktail = cocktail_repository.get_cocktail_by_id(id)
    if cocktail is None:
        from werkzeug.exceptions import abort
        abort(404, "Cocktail non trovato.")

    # aggiungi nome tipo
    type_obj = None
    if cocktail.get('cocktail_type_id'):
        types = cocktail_type_repository.get_all_cocktail_types()
        for t in types:
            if t['id'] == cocktail['cocktail_type_id']:
                type_obj = t
                break

    return render_template('cocktail_detail.html', cocktail=cocktail, type=type_obj)


@bp.route('/cocktails/create', methods=('GET', 'POST'))
def create_cocktail():
    """Crea un nuovo cocktail; può ricevere ingredienti multipli tramite campi ripetuti."""
    types = cocktail_type_repository.get_all_cocktail_types()
    ingredients = ingredient_repository.get_all_ingredients()

    if request.method == 'POST':
        name = request.form.get('name')
        country = request.form.get('country')
        region = request.form.get('region')
        preparation_time_minutes = request.form.get('preparation_time_minutes', type=int)
        cocktail_type_id = request.form.get('cocktail_type_id', type=int)
        instructions = request.form.get('instructions')
        image_url = request.form.get('image_url')

        error = None
        if not name:
            error = 'Il nome è obbligatorio.'

        if error is not None:
            flash(error)
        else:
            # leggi eventuali ingredienti passati come liste
            ingredient_ids = request.form.getlist('ingredient_id')
            quantities = request.form.getlist('quantity')
            units = request.form.getlist('unit')
            ing_list = []
            for iid, q, u in zip(ingredient_ids, quantities, units):
                try:
                    iid_i = int(iid)
                    q_f = float(q)
                except Exception:
                    continue
                ing_list.append({'ingredient_id': iid_i, 'quantity': q_f, 'unit': u or None})

            cocktail_id = cocktail_repository.create_cocktail(
                name, country, region, preparation_time_minutes, cocktail_type_id, instructions, image_url=image_url, ingredients=ing_list
            )
            return redirect(url_for('main.search_cocktails'))

    return render_template('create_cocktail.html', types=types, ingredients=ingredients)

