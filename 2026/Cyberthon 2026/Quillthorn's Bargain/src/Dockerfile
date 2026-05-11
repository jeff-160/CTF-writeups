FROM php:8.3.11-fpm

RUN apt-get update && \
    apt-get install -y --no-install-recommends \
        nginx \
        libnginx-mod-http-lua \
        supervisor && \
    rm -rf /var/lib/apt/lists/*

COPY nginx/default.conf /etc/nginx/sites-available/default
COPY php/ /var/www/html/
COPY flag.txt /flag.txt

RUN chown root:root /flag.txt && chmod 444 /flag.txt

RUN mkdir -p /var/lib/php/sessions && \
    chown www-data:www-data /var/lib/php/sessions && \
    chmod 700 /var/lib/php/sessions

COPY supervisord.conf /etc/supervisor/conf.d/supervisord.conf

EXPOSE 80

CMD ["/usr/bin/supervisord", "-c", "/etc/supervisor/conf.d/supervisord.conf"]
