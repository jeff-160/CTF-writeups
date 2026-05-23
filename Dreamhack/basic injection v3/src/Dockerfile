
FROM python:3.10-slim

RUN apt-get update && apt-get install -y --no-install-recommends sqlite3 && rm -rf /var/lib/apt/lists/*

RUN adduser --disabled-password --gecos '' appuser
WORKDIR /app

RUN pip install --no-cache-dir --upgrade pip
RUN pip install --no-cache-dir flask python-dotenv

COPY app.py middleware.py ./
COPY templates ./templates/
COPY flag /
RUN chmod 777 /app

RUN chown -R appuser:appuser /app
USER appuser

ENV FLASK_APP=app.py
EXPOSE 5000
CMD ["python", "app.py"]