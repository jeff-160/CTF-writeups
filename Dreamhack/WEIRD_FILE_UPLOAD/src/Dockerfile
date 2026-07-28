FROM php:7.3-apache
ARG DEBIAN_FRONTEND=noninteractive
ENV TZ=Asia/Seoul
RUN chmod -R 755 /etc/apache2 && \
    chown -R root:root /var/www && \
    chmod -R 755 /var/www
RUN apt-get update && apt-get install -y gcc
RUN rm /var/log/apache2/access.log /var/log/apache2/error.log /var/log/apache2/other_vhosts_access.log
RUN openssl rand -hex 32 > /seed.txt && \
    chown root:root /seed.txt && \
    chmod 444 /seed.txt
COPY html /var/www/html
RUN chown -R root:root /var/www/html && \
    chmod -R 555 /var/www/html
RUN gcc -o /flag /var/www/html/flag.c && \
    chmod 111 /flag && \
    rm /var/www/html/flag.c
    
RUN mkdir -p /var/www/html/uploads && \
    chown -R www-data:www-data /var/www/html/uploads && \
    chmod -R 333 /var/www/html/uploads
COPY ./config/php.ini /usr/local/etc/php/php.ini

RUN chmod -R 555 /var/log/apache2 && \
    touch /var/log/apache2/access.log /var/log/apache2/error.log /var/log/apache2/other_vhosts_access.log && \
    chmod 644 /var/log/apache2/access.log /var/log/apache2/error.log /var/log/apache2/other_vhosts_access.log

EXPOSE 80
CMD while true; do find /var/www/html/uploads/ -mindepth 1 -delete; sleep 10s; done & \
    apache2-foreground