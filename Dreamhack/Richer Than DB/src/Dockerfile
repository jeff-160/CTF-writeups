FROM python:3.9-slim
RUN apt-get update && apt-get install -y nginx
WORKDIR /app

COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt

COPY deploy /app

COPY nginx.conf /etc/nginx/nginx.conf

CMD service nginx start && python -u /app/app.py
