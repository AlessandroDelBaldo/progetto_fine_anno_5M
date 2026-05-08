# Cocktail App

Cocktail App è un'applicazione web che consente di gestire cocktail: puoi consultare i cocktail esistenti, crearne di nuovi e associare ingredienti con quantità (grammi o ml).

L'applicazione utilizza il framework web Flask e il database SQLite. Per l'interfaccia utente, vengono utilizzati i template HTML Jinja2 e i CSS per il layout e lo stile.

Il percorso file dell'applicazione segue la seguente struttura:
- `app/`: contiene i file di codice Python dell'applicazione
- `app/templates/`: contiene i template HTML utilizzati dall'applicazione
- `app/static/`: contiene i file CSS e le immagini utilizzati dall'applicazione
- `run.py`: file eseguibile che avvia l'applicazione
- `tools/`: contiene gli script utilizzati per popolare il database con i dati dell'API
- `instance/`: contiene il database SQLite e i file di configurazione dell'applicazione

L'applicazione utilizza l'API di TheCocktailDB per recuperare i dati sui cocktail. L'API offre endpoint per la ricerca di cocktail per nome, per lettera, per ingrediente e per ID.

## Come avviare l'applicazione

### 1. Installa le dipendenze

```bash
pip install -r requirements.txt
```

### 2. Crea il database

Esegui lo script dalla root del progetto per creare le tabelle e inserire i dati di esempio:

```bash
python tools/setup_db.py
```

### 3. Popola il database dall'API

Per importare tutti i cocktail da TheCocktailDB (richiede connessione internet):

```bash
python tools/populate_from_api.py
```

### 4. Avvia il server

```bash
python run.py
```

L'applicazione sarà disponibile su [http://127.0.0.1:5001](http://127.0.0.1:5001).

> Per cambiare host o porta, imposta le variabili d'ambiente `FLASK_RUN_HOST` e `FLASK_RUN_PORT` prima di avviare.
