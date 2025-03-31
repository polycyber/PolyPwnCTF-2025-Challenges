#!/bin/bash

# Fonction pour obtenir un port inutilisé
get_unused_port() {
    python3 -c 'import socket; s = socket.socket(); s.bind(("", 0)); print(s.getsockname()[1]); s.close()'
}

# Obtenir un port inutilisé
PORT=$(get_unused_port)

# Exécuter app.py avec le port en argument
exec python3 /app/app.py "$PORT"
