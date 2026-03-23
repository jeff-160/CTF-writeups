FROM fedora:latest

RUN dnf install -y httpd python3 python3-pip ffmpeg mod_wsgi openssl && \
    pip3 install flask werkzeug

RUN mkdir -p /srv/app /srv/http/uploads/admin /srv/http/static/frames/shared/bad-apple

COPY wsgi_app.py /srv/app/wsgi_app.py
COPY templates/ /srv/app/templates/

COPY uploads/ /srv/http/uploads/
COPY bad-apple-frames/ /srv/http/static/frames/shared/bad-apple/
COPY .htpasswd /srv/http/.htpasswd
COPY httpd-append.conf /tmp/httpd-append.conf

RUN cat /tmp/httpd-append.conf >> /etc/httpd/conf/httpd.conf && \
    chmod -R 755 /srv/http/uploads /srv/http/static && \
    chown -R apache:apache /srv/app /srv/http

EXPOSE 80

CMD ["sh", "-c", "HEX=$(openssl rand -hex 16) && mv /srv/http/uploads/admin/flag.gif /srv/http/uploads/admin/$HEX-flag.gif && echo $HEX > /srv/http/.flag_secret && httpd -DFOREGROUND"]
