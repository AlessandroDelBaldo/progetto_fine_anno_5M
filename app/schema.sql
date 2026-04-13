-- ############################################################
-- Schema per i COCKTAIL, TIPI e INGREDIENTI
-- Requisiti coperti:
-- - cocktail con nome, provenienza (stato e regione), tempo di preparazione
-- - ingredienti come lista tramite tabella many-to-many con quantità
-- - costo calcolato come somma(quantity * cost_per_unit) tramite VIEW
-- ############################################################

DROP TABLE IF EXISTS cocktail_ingredients;
DROP TABLE IF EXISTS cocktails;
DROP TABLE IF EXISTS ingredients;
DROP TABLE IF EXISTS cocktail_types;

CREATE TABLE cocktail_types (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  name TEXT NOT NULL UNIQUE,
  description TEXT
);

CREATE TABLE ingredients (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  name TEXT NOT NULL UNIQUE,
  default_unit TEXT NOT NULL,
  image_url TEXT
);

CREATE TABLE cocktails (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  name TEXT NOT NULL,
  country TEXT,
  region TEXT,
  preparation_time_minutes INTEGER,
  cocktail_type_id INTEGER,
  instructions TEXT,
  image_url TEXT,
  api_id TEXT UNIQUE,
  abv REAL,
  FOREIGN KEY (cocktail_type_id) REFERENCES cocktail_types (id)
);

-- Tabella di relazione many-to-many che contiene la quantità necessaria per ogni ingrediente
CREATE TABLE cocktail_ingredients (
  cocktail_id INTEGER NOT NULL,
  ingredient_id INTEGER NOT NULL,
  quantity REAL NOT NULL, -- quantità nell'unità specificata
  unit TEXT, -- opzionale: sovrascrive ingredients.default_unit se presente
  PRIMARY KEY (cocktail_id, ingredient_id),
  FOREIGN KEY (cocktail_id) REFERENCES cocktails (id) ON DELETE CASCADE,
  FOREIGN KEY (ingredient_id) REFERENCES ingredients (id)
);

-- View che calcola il costo totale di un cocktail come somma di (quantity * cost_per_unit)
-- Nota: la view assume che le unità siano coerenti tra quantity e cost_per_unit (es. costo per grammo e quantità in grammi).
-- Nota: il calcolo del costo non è più memorizzato nel DB (colonna cost_per_unit rimossa).
-- Se vuoi conservare un costo totale per cocktail, considera di aggiungere una colonna materializzata
-- o calcolare il costo lato applicazione usando i prezzi esterni.

-- Esempi di inserimento (demo)
INSERT INTO cocktail_types (name, description) VALUES ('Classico', 'Cocktail tradizionali');
INSERT INTO cocktail_types (name, description) VALUES ('Tropicale', 'Cocktail con frutta tropicale');
INSERT INTO cocktail_types (name, description) VALUES ('Senza alcool', 'Cocktail analcolici');

INSERT INTO ingredients (name, default_unit, image_url) VALUES ('Vodka', 'ml', NULL);
INSERT INTO ingredients (name, default_unit, image_url) VALUES ('Succo di limone', 'ml', NULL);
INSERT INTO ingredients (name, default_unit, image_url) VALUES ('Zucchero', 'g', NULL);
INSERT INTO ingredients (name, default_unit, image_url) VALUES ('Ghiaccio', 'pcs', NULL);

-- Esempio di cocktail
INSERT INTO cocktails (name, country, region, preparation_time_minutes, cocktail_type_id, instructions, image_url) VALUES
('Mojito', 'Cuba', 'Havana', 5, 1, 'Mescolare ingredienti e servire con ghiaccio.', NULL);

-- Associare ingredienti al cocktail (quantità in unità coerenti con default_unit)
-- Mojito: 50ml vodka, 20ml succo di limone, 10g zucchero, 5 pcs ghiaccio
INSERT INTO cocktail_ingredients (cocktail_id, ingredient_id, quantity, unit) VALUES (1, 1, 50, 'ml');
INSERT INTO cocktail_ingredients (cocktail_id, ingredient_id, quantity, unit) VALUES (1, 2, 20, 'ml');
INSERT INTO cocktail_ingredients (cocktail_id, ingredient_id, quantity, unit) VALUES (1, 3, 10, 'g');
INSERT INTO cocktail_ingredients (cocktail_id, ingredient_id, quantity, unit) VALUES (1, 4, 5, 'pcs');

-- Fine schema cocktail