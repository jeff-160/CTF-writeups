FROM php:7.4-apache

RUN apt-get update && apt-get install -y inotify-tools && rm -rf /var/lib/apt/lists/*

WORKDIR /var/www/html

COPY src/index.php /var/www/html/

COPY start.sh /usr/local/bin/start.sh

RUN echo "THJCC{fake_flag_for_test}" > /flag.txt

RUN chmod +x /usr/local/bin/start.sh

RUN chown root:www-data /var/www/html && chmod 1775 /var/www/html

RUN chown root:root /var/www/html/index.php && chmod 444 /var/www/html/index.php

ENTRYPOINT ["/usr/local/bin/start.sh"]
