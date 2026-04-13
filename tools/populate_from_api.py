"""
Script per popolare il database con i cocktail da TheCocktailDB API.
TheCocktailDB: https://www.thecocktaildb.com/api/
"""

import requests
import sqlite3
from pathlib import Path
import time

# Configurazione
API_BASE = "https://www.thecocktaildb.com/api/json/v1/1"
COCKTAILS_ENDPOINT = f"{API_BASE}/search.php?f="  # Cerca per prima lettera
INGREDIENT_ENDPOINT = f"{API_BASE}/search.php?i="  # Cerca ingrediente

repo_root = Path(__file__).resolve().parents[1]
db_path = repo_root / 'instance' / 'cocktails.sqlite'


def get_cocktail_type_id(db, category):
    """Ottiene o crea il tipo di cocktail."""
    if not category:
        return None
    
    cursor = db.execute("SELECT id FROM cocktail_types WHERE name = ?", (category,))
    result = cursor.fetchone()
    
    if result:
        return result[0]
    else:
        # Crea un nuovo tipo se non esiste
        cursor = db.execute(
            "INSERT INTO cocktail_types (name, description) VALUES (?, ?)",
            (category, f"Categoria: {category}")
        )
        db.commit()
        return cursor.lastrowid


def get_or_create_ingredient(db, name, unit="ml"):
    """Ottiene o crea un ingrediente."""
    cursor = db.execute("SELECT id FROM ingredients WHERE name = ?", (name,))
    result = cursor.fetchone()
    
    if result:
        return result[0]
    else:
        cursor = db.execute(
            "INSERT INTO ingredients (name, default_unit, image_url) VALUES (?, ?, ?)",
            (name, unit, None)
        )
        db.commit()
        return cursor.lastrowid


def fetch_cocktails():
    """Recupera i cocktail da TheCocktailDB."""
    print("🍹 Recuperando cocktail da TheCocktailDB...")
    cocktails = []
    
    # Cerca cocktail per ogni lettera (A-Z)
    for letter in "abcdefghijklmnopqrstuvwxyz":
        try:
            url = f"{COCKTAILS_ENDPOINT}{letter}"
            response = requests.get(url, timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                if data.get('drinks'):
                    cocktails.extend(data['drinks'])
                    print(f"  ✓ Lettera '{letter.upper()}': {len(data['drinks'])} cocktail")
                time.sleep(0.1)  # Piccolo delay per non sovraccaricare l'API
            else:
                print(f"  ✗ Errore lettera '{letter.upper()}': {response.status_code}")
        except Exception as e:
            print(f"  ✗ Errore durante fetch lettera '{letter.upper()}': {e}")
    
    print(f"\n📊 Totale cocktail recuperati: {len(cocktails)}")
    return cocktails


def insert_cocktails(db, cocktails):
    """Inserisce i cocktail nel database."""
    print("\n💾 Inserendo cocktail nel database...")
    inserted = 0
    skipped = 0
    
    for cocktail in cocktails:
        try:
            # Controlla se il cocktail esiste già
            api_id = cocktail.get('idDrink')
            cursor = db.execute("SELECT id FROM cocktails WHERE api_id = ?", (api_id,))
            if cursor.fetchone():
                skipped += 1
                continue
            
            name = cocktail.get('strDrink', 'Unknown')
            category = cocktail.get('strCategory', 'Cocktail')
            instructions = cocktail.get('strInstructions', '')
            image_url = cocktail.get('strDrinkThumb', None)
            abv = cocktail.get('strABV')
            abv_value = None
            if abv:
                try:
                    abv_value = float(abv.replace('%', ''))
                except:
                    abv_value = None
            
            # Ottieni il tipo di cocktail
            cocktail_type_id = get_cocktail_type_id(db, category)
            
            # Inserisci il cocktail
            cursor = db.execute(
                """INSERT INTO cocktails 
                   (name, country, region, cocktail_type_id, instructions, image_url, api_id, abv)
                   VALUES (?, ?, ?, ?, ?, ?, ?, ?)""",
                (name, cocktail.get('strIBA'), None, cocktail_type_id, instructions, image_url, api_id, abv_value)
            )
            cocktail_id = cursor.lastrowid
            
            # Inserisci gli ingredienti
            for i in range(1, 16):  # TheCocktailDB ha max 15 ingredienti
                ingredient_name = cocktail.get(f'strIngredient{i}')
                ingredient_measure = cocktail.get(f'strMeasure{i}')
                
                if ingredient_name:
                    ingredient_id = get_or_create_ingredient(db, ingredient_name, "ml")
                    
                    # Estrai quantità e unità da strMeasure (es. "1.5 oz" -> 1.5 e "oz")
                    quantity = 1.0
                    unit = "ml"
                    
                    if ingredient_measure:
                        parts = ingredient_measure.strip().split()
                        if parts:
                            try:
                                quantity = float(parts[0])
                                if len(parts) > 1:
                                    unit = " ".join(parts[1:])
                            except:
                                quantity = 1.0
                    
                    db.execute(
                        """INSERT INTO cocktail_ingredients 
                           (cocktail_id, ingredient_id, quantity, unit)
                           VALUES (?, ?, ?, ?)""",
                        (cocktail_id, ingredient_id, quantity, unit)
                    )
            
            db.commit()
            inserted += 1
            
            if inserted % 10 == 0:
                print(f"  ✓ Inseriti {inserted} cocktail...")
        
        except Exception as e:
            name = cocktail.get('strDrink', 'Unknown')
            print(f"  ✗ Errore inserimento cocktail '{name}': {e}")
            db.rollback()
    
    print(f"\n✅ Cocktail inseriti: {inserted}")
    print(f"⏭️  Cocktail saltati (duplicati): {skipped}")
    return inserted


def main():
    print("=" * 60)
    print("  POPOLA DATABASE DA TheCocktailDB")
    print("=" * 60)
    
    # Recupera i cocktail dall'API
    cocktails = fetch_cocktails()
    
    if not cocktails:
        print("❌ Nessun cocktail recuperato!")
        return
    
    # Connettiti al database
    try:
        db = sqlite3.connect(str(db_path))
        db.row_factory = sqlite3.Row
        
        # Inserisci i cocktail
        inserted = insert_cocktails(db, cocktails)
        db.close()
        
        print("\n" + "=" * 60)
        print("  ✅ POPOLO COMPLETATO AVEC SUCCESSO!")
        print("=" * 60)
        
    except Exception as e:
        print(f"❌ Errore: {e}")
        if 'db' in locals():
            db.close()


if __name__ == "__main__":
    main()
