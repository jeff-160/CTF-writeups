FROM node:18-bullseye-slim

RUN apt update && apt install -y php7.4 apache2 wget gnupg \
  && wget -q -O - https://dl-ssl.google.com/linux/linux_signing_key.pub | apt-key add - \ 
  && echo "deb http://dl.google.com/linux/chrome/deb/ stable main" >> /etc/apt/sources.list.d/google.list \
  && apt update && apt install -y --no-install-recommends google-chrome-stable \
  && rm -rf /var/lib/apt/lists/*

COPY html /var/www/html
COPY flag /flag
COPY bot /bot

WORKDIR /bot
RUN npm install
RUN rm /var/www/html/index.html \
  && mkdir /var/www/html/files \
  && chown -R www-data:www-data /var/www/html

EXPOSE 80

ENTRYPOINT ["/usr/sbin/apache2ctl", "-D", "FOREGROUND"]