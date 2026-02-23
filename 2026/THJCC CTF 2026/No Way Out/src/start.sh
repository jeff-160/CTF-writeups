#!/bin/bash

(
    inotifywait -m -r -e create --format '%w%f' /var/www/html | while read NEWFILE
    do
        if [ "$(basename "$NEWFILE")" != "index.php" ]; then
            sleep 0.67 
            rm -f "$NEWFILE"
        fi
    done
) &

exec docker-php-entrypoint apache2-foreground
