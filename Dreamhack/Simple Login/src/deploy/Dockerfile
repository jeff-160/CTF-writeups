FROM node:21.5-slim@sha256:c88704924204ee6d4e9da02275a8fd27355502f7177e4175cd0d3a4375a9c9c8

ARG DEBIAN_FRONTEND=noninteractive
ENV NODE_ENV production
ENV PORT 7000
ENV USER app

# Install packages
RUN apt update && \
    apt install -y \
    tzdata \
    openssl
RUN ln -sf /usr/share/zoneinfo/Asia/Seoul /etc/localtime
RUN dpkg-reconfigure tzdata

# Add user
RUN adduser --disabled-password --gecos "" --uid 1001 $USER

# Set working directory
RUN mkdir /app
WORKDIR /app

# Add files
COPY --chown=root:root app/server.js /app/
COPY --chown=root:root app/views /app/views
COPY --chown=root:root flag /
COPY --chown=root:root app/package.json /app/
COPY --chown=root:root app/package-lock.json /app/

# Install dependencies
RUN npm install

# Newly generate keys
RUN openssl genrsa -out /priv.pem 2048
RUN openssl rsa -in /priv.pem -pubout -out /pub.crt

RUN chmod 644 /flag
RUN chmod 644 /priv.pem
RUN chmod 644 /pub.crt

USER $USER
EXPOSE $PORT
CMD while :; do sleep 0.5; node server.js; done
