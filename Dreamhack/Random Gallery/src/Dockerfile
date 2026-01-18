FROM python:3.11-slim

ENV PORT=80
ENV FLAG=DH{FAKE_FLAG}

RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential python3-dev libpcre2-dev nginx && \
    rm -rf /var/lib/apt/lists/*

RUN rm -f /etc/nginx/sites-enabled/default
COPY ./nginx/nginx.conf /etc/nginx/conf.d/default.conf

WORKDIR /app
COPY ./app /app
RUN pip install -r requirements.txt
EXPOSE 80

CMD ["sh", "-c", "service nginx start && uwsgi --http 0.0.0.0:3000 --module main:app"]