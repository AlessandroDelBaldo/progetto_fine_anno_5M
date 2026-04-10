# Importiamo la funzione create_app dal pacchetto 'app'
# Questo è possibile perché 'app' ha un file __init__.py!
from app import create_app
import os


# Chiamiamo la fabbrica per ottenere l'applicazione
app = create_app()


def _get_env(name, default=None):
    v = os.environ.get(name)
    return v if v is not None else default


# Se questo file viene eseguito direttamente (non importato), avvia il server
if __name__ == "__main__":
    # Parametri eseguibili da env: FLASK_RUN_HOST, FLASK_RUN_PORT
    host = _get_env('FLASK_RUN_HOST', '127.0.0.1')
    port = int(_get_env('FLASK_RUN_PORT', 5001))
    debug = app.config.get('DEBUG', True)
    app.run(host=host, port=port, debug=debug)
