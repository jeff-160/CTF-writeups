FROM python:3.11-alpine@sha256:610ede222c1fa9675c694c99429f8d2c1b4e243f1982246da9e540eb5800ee4a

RUN apk --update add socat \
	&& pip3 install cryptography==46.0.2 \
	&& adduser -D --home /app user

COPY --chown=user chall.py entry.sh flag.txt /app

RUN chmod 755 /app/entry.sh /app/chall.py

WORKDIR /app

EXPOSE ${LISTEN_PORT}

ENTRYPOINT ["/app/entry.sh"]
