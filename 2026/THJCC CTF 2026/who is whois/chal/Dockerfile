FROM python:3.9-slim-bullseye

RUN apt-get update && apt-get install -y whois && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY app.py .

EXPOSE 13316

CMD ["gunicorn", "-b", "0.0.0.0:13316", "app:app"]
