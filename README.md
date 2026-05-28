# CocktailHub

CocktailHub è un'applicazione web per gestire un ricettario di cocktail: puoi consultare i cocktail esistenti, cercarli per nome o ingrediente, crearne di nuovi e associare ingredienti con quantità e unità di misura (es. ml, g, pz).

L'applicazione è sviluppata con **Python** e **Flask**, utilizza **SQLite** come database e i template **Jinja2** per l'interfaccia utente.

## Struttura del progetto

```
progetto_fine_anno_5M/
├── app/                        # Codice Python dell'applicazione
│   ├── __init__.py             # Factory dell'app Flask
│   ├── main.py                 # Blueprint principale con le route
│   ├── db.py                   # Gestione connessione al database
│   ├── repositories/           # Repository per l'accesso ai dati
│   │   ├── cocktail_repository.py
│   │   ├── cocktail_type_repository.py
│   │   ├── cocktail_ingredient_repository.py
│   │   └── ingredient_repository.py
│   ├── templates/              # Template HTML Jinja2
│   └── static/                 # CSS e immagini
├── tools/                      # Script di utilità
│   ├── setup_db.py             # Crea le tabelle del database
│   └── populate_from_api.py    # Popola il DB da TheCocktailDB
├── instance/                   # Database SQLite (generato automaticamente)
├── run.py                      # Avvio dell'applicazione
└── requirements.txt            # Dipendenze Python
```

## Route disponibili

| URL | Descrizione |
|-----|-------------|
| `/` | Home: lista cocktail con ricerca integrata |
| `/search?q=<testo>` | Ricerca cocktail per nome o ingrediente |
| `/cocktails` | Elenco completo di tutti i cocktail |
| `/cocktails/<id>` | Dettaglio cocktail con ingredienti |
| `/cocktails/create` | Form per creare un nuovo cocktail |

## Come avviare l'applicazione

### 1. Installa le dipendenze

```bash
pip install -r requirements.txt
```

### 2. Crea il database

```bash
python tools/setup_db.py
```

### 3. (Opzionale) Popola il database dall'API

Per importare cocktail reali da TheCocktailDB (richiede connessione internet):

```bash
python tools/populate_from_api.py
```

> Questo script è separato dall'app. L'applicazione stessa non chiama API esterne durante il normale funzionamento.

### 4. Avvia il server

```bash
python run.py
```

L'applicazione sarà disponibile su [http://127.0.0.1:5001](http://127.0.0.1:5001).

> Per cambiare host o porta, imposta le variabili d'ambiente `FLASK_RUN_HOST` e `FLASK_RUN_PORT` prima di avviare.
