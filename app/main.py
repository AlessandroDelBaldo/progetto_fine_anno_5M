from flask import Blueprint, flash, redirect, render_template, request, url_for
from app.repositories import recipe_repository, ingredient_repository, recipe_type_repository

# Usiamo 'main' perché è il blueprint principale del sito
bp = Blueprint("main", __name__)


@bp.route("/")
def index():
    # Mostra direttamente la lista delle ricette (landing principale)
    recipes = recipe_repository.get_all_recipes()
    types = {t['id']: t['name'] for t in recipe_type_repository.get_all_recipe_types()}
    for r in recipes:
        r['type_name'] = types.get(r.get('recipe_type_id'))
    return render_template('recipes_list.html', recipes=recipes)


@bp.route('/recipes')
def search_recipes():
    """Lista tutte le ricette disponibili."""
    recipes = recipe_repository.get_all_recipes()
    # arricchisci con tipo di ricetta (nome)
    types = {t['id']: t['name'] for t in recipe_type_repository.get_all_recipe_types()}
    for r in recipes:
        r['type_name'] = types.get(r.get('recipe_type_id'))
    return render_template('recipes_list.html', recipes=recipes)


@bp.route('/recipes/<int:id>')
def recipe_detail(id):
    """Mostra i dettagli di una singola ricetta."""
    recipe = recipe_repository.get_recipe_by_id(id)
    if recipe is None:
        from werkzeug.exceptions import abort
        abort(404, "Ricetta non trovata.")

    # aggiungi nome tipo
    type_obj = None
    if recipe.get('recipe_type_id'):
        types = recipe_type_repository.get_all_recipe_types()
        for t in types:
            if t['id'] == recipe['recipe_type_id']:
                type_obj = t
                break

    return render_template('recipe_detail.html', recipe=recipe, type=type_obj)


@bp.route('/recipes/create', methods=('GET', 'POST'))
def create_recipe():
    """Crea una nuova ricetta; può ricevere ingredienti multipli tramite campi ripetuti."""
    types = recipe_type_repository.get_all_recipe_types()
    ingredients = ingredient_repository.get_all_ingredients()

    if request.method == 'POST':
        name = request.form.get('name')
        country = request.form.get('country')
        region = request.form.get('region')
        preparation_time_minutes = request.form.get('preparation_time_minutes', type=int)
        recipe_type_id = request.form.get('recipe_type_id', type=int)
        instructions = request.form.get('instructions')

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

            recipe_id = recipe_repository.create_recipe(
                name, country, region, preparation_time_minutes, recipe_type_id, instructions, ingredients=ing_list
            )
            return redirect(url_for('main.search_recipes'))

    return render_template('create_recipe.html', types=types, ingredients=ingredients)

