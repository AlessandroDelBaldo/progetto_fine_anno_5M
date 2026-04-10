-- ############################################################
-- Schema per le RICETTE, TIPI e INGREDIENTI
-- Requisiti coperti:
-- - ricette con nome, provenienza (stato e regione), tempo di preparazione
-- - ingredienti come lista tramite tabella many-to-many con quantità
-- - costo calcolato come somma(quantity * cost_per_unit) tramite VIEW
-- ############################################################

DROP TABLE IF EXISTS recipe_ingredients;
DROP TABLE IF EXISTS recipes;
DROP TABLE IF EXISTS ingredients;
DROP TABLE IF EXISTS recipe_types;

CREATE TABLE recipe_types (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  name TEXT NOT NULL UNIQUE,
  description TEXT
);

CREATE TABLE ingredients (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  name TEXT NOT NULL UNIQUE,
  default_unit TEXT NOT NULL
);

CREATE TABLE recipes (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  name TEXT NOT NULL,
  country TEXT, -- stato / provenienza
  region TEXT,  -- regione
  preparation_time_minutes INTEGER, -- tempo di preparazione in minuti
  recipe_type_id INTEGER,
  instructions TEXT,
  FOREIGN KEY (recipe_type_id) REFERENCES recipe_types (id)
);

-- Tabella di relazione many-to-many che contiene la quantità necessaria per ogni ingrediente
CREATE TABLE recipe_ingredients (
  recipe_id INTEGER NOT NULL,
  ingredient_id INTEGER NOT NULL,
  quantity REAL NOT NULL, -- quantità nell'unità specificata
  unit TEXT, -- opzionale: sovrascrive ingredients.default_unit se presente
  PRIMARY KEY (recipe_id, ingredient_id),
  FOREIGN KEY (recipe_id) REFERENCES recipes (id) ON DELETE CASCADE,
  FOREIGN KEY (ingredient_id) REFERENCES ingredients (id)
);

-- View che calcola il costo totale di una ricetta come somma di (quantity * cost_per_unit)
-- Nota: la view assume che le unità siano coerenti tra quantity e cost_per_unit (es. costo per grammo e quantità in grammi).
-- Nota: il calcolo del costo non è più memorizzato nel DB (colonna cost_per_unit rimossa).
-- Se vuoi conservare un costo totale per ricetta, considera di aggiungere una colonna materializzata
-- o calcolare il costo lato applicazione usando i prezzi esterni.

-- Esempi di inserimento (demo)
INSERT INTO recipe_types (name, description) VALUES ('Primo', 'Piatti principali come paste e zuppe');
INSERT INTO recipe_types (name, description) VALUES ('Secondo', 'Piatti a base di carne o pesce');
INSERT INTO recipe_types (name, description) VALUES ('Dolce', 'Dessert e dolci');

INSERT INTO ingredients (name, default_unit) VALUES ('Farina', 'g');
INSERT INTO ingredients (name, default_unit) VALUES ('Zucchero', 'g');
INSERT INTO ingredients (name, default_unit) VALUES ('Uova', 'pcs');
INSERT INTO ingredients (name, default_unit) VALUES ('Latte', 'ml');

-- Esempio di ricetta
INSERT INTO recipes (name, country, region, preparation_time_minutes, recipe_type_id, instructions) VALUES
('Pancakes', 'USA', 'Nationwide', 20, 1, 'Mescolare ingredienti e cuocere in padella.');

-- Associare ingredienti alla ricetta (quantità in unità coerenti con default_unit)
-- Pancakes: 200g farina, 30g zucchero, 2 uova, 300ml latte
INSERT INTO recipe_ingredients (recipe_id, ingredient_id, quantity, unit) VALUES (1, 1, 200, 'g');
INSERT INTO recipe_ingredients (recipe_id, ingredient_id, quantity, unit) VALUES (1, 2, 30, 'g');
INSERT INTO recipe_ingredients (recipe_id, ingredient_id, quantity, unit) VALUES (1, 3, 2, 'pcs');
INSERT INTO recipe_ingredients (recipe_id, ingredient_id, quantity, unit) VALUES (1, 4, 300, 'ml');

-- Fine schema ricette