#!/bin/bash
set -e

# Hand off to mariadb's docker-entrypoint so it initialises /var/lib/mysql
# and applies /docker-entrypoint-initdb.d/* on first boot, then exec node.
docker-entrypoint.sh mariadbd &

# Wait for the DB to be ready.
until mariadb -uroot -p"$MARIADB_ROOT_PASSWORD" -e 'SELECT 1' >/dev/null 2>&1; do
    sleep 0.5
done

# Give init scripts a moment to finish if they're still running.
until mariadb -u"$MARIADB_USER" -p"$MARIADB_PASSWORD" "$MARIADB_DATABASE" \
        -e 'SELECT 1 FROM accounts LIMIT 1' >/dev/null 2>&1; do
    sleep 0.5
done

exec node /app/index.js
