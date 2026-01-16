FROM php:8.1-apache

COPY ./deploy/run.sh /usr/sbin/
RUN chmod +x /usr/sbin/run.sh

COPY ./deploy/src /var/www/html/

COPY ./deploy/flag.txt /

EXPOSE 80
CMD ["/usr/sbin/run.sh"]