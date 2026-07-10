#!/bin/sh
set -eu

APP_HOST="127.0.0.1"
APP_PORT="18080"
WAF_HOST="0.0.0.0"
WAF_PORT="8080"
WAF_GUARD="/waf_guard"

if [ ! -x "$WAF_GUARD" ]; then
    echo "[-] missing WAF guard: $WAF_GUARD" >&2
    exit 1
fi

echo "[+] starting web service on $APP_HOST:$APP_PORT"
APP_HOST="$APP_HOST" APP_PORT="$APP_PORT" python3 /app/app.py &
app_child="$!"

ready=0
tries=0
while [ "$tries" -lt 50 ]; do
    if APP_HOST="$APP_HOST" APP_PORT="$APP_PORT" python3 -c 'import os, socket; sock = socket.create_connection((os.environ["APP_HOST"], int(os.environ["APP_PORT"])), 0.2); sock.close()' >/dev/null 2>&1; then
        ready=1
        break
    fi
    tries=$((tries + 1))
    sleep 0.1
done

if [ "$ready" -ne 1 ]; then
    echo "[-] web service did not become ready" >&2
    exit 1
fi

echo "[+] starting WAF guard on $WAF_HOST:$WAF_PORT"
"$WAF_GUARD" "$WAF_HOST" "$WAF_PORT" "$APP_HOST" "$APP_PORT" &
waf_child="$!"

cleanup() {
    kill "$waf_child" >/dev/null 2>&1 || true
    kill "$app_child" >/dev/null 2>&1 || true
    wait "$waf_child" >/dev/null 2>&1 || true
    wait "$app_child" >/dev/null 2>&1 || true
}

trap cleanup INT TERM EXIT
wait "$waf_child"
