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
