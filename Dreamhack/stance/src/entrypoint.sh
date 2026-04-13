#!/bin/sh
set -e

# Ensure flag is set
if [ -z "$FLAG" ]; then
    echo "[warn] FLAG environment variable not set, using default"
    export FLAG="flag{test_flag}"
fi

echo "[entrypoint] Starting XSS-Insane on port 3000..."
exec python app.py
