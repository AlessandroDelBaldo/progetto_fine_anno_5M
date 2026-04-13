from pathlib import Path
import sqlite3

repo_root = Path(__file__).resolve().parents[1]
schema_path = repo_root / 'app' / 'schema.sql'
db_path = repo_root / 'test_cocktails.db'

# Remove existing test DB if present
if db_path.exists():
    db_path.unlink()

sql = schema_path.read_text(encoding='utf-8')

conn = sqlite3.connect(str(db_path))
conn.row_factory = sqlite3.Row
cur = conn.cursor()

print('Applying schema from', schema_path)
cur.executescript(sql)
conn.commit()

def q(qs, params=()):
    print('\n-- QUERY:', qs)
    rows = cur.execute(qs, params).fetchall()
    print(f'Rows: {len(rows)}')
    for r in rows:
        print(dict(r))

q('SELECT id, name, description FROM cocktail_types')
q('SELECT id, name, default_unit, image_url FROM ingredients')
q('SELECT id, name, country, region, preparation_time_minutes, cocktail_type_id, instructions, image_url FROM cocktails')
q("SELECT ci.cocktail_id, i.name as ingredient_name, ci.quantity, ci.unit FROM cocktail_ingredients ci JOIN ingredients i ON i.id = ci.ingredient_id")

conn.close()
print('\nTest DB created at', db_path)
