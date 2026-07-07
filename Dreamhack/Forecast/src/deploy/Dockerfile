FROM mariadb:11

ENV MARIADB_ROOT_PASSWORD=rootpw
ENV MARIADB_DATABASE=forecast
ENV MARIADB_USER=forecast
ENV MARIADB_PASSWORD=forecastpw

RUN apt-get update \
 && apt-get install -y --no-install-recommends curl ca-certificates \
 && curl -fsSL https://deb.nodesource.com/setup_20.x | bash - \
 && apt-get install -y --no-install-recommends nodejs \
 && apt-get clean \
 && rm -rf /var/lib/apt/lists/*

WORKDIR /app
COPY package.json ./
RUN npm install --omit=dev

COPY index.js ./
COPY seed ./seed
COPY schema.sql /docker-entrypoint-initdb.d/001-schema.sql
COPY start.sh /usr/local/bin/start.sh
COPY flag.txt /flag.txt
RUN chmod +x /usr/local/bin/start.sh

RUN mkdir -p /srv/releases /srv/uploads

EXPOSE 3000
CMD ["/usr/local/bin/start.sh"]