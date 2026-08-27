FROM python:3.11-slim

WORKDIR /app

ENV PYTHONUNBUFFERED=1

RUN pip install flask

COPY . .

RUN FLAG="flag-$(head -c 80 /dev/urandom | tr -dc A-Za-z0-9 | head -c 8).txt" && mv ./flag.txt /$FLAG

CMD ["python", "app.py"]