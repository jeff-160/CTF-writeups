FROM python:3.11-slim

WORKDIR /app

COPY deploy/requirements.txt .
COPY deploy/app.py .
COPY deploy/templates ./templates
COPY deploy/static ./static
COPY deploy/fruits.db .

RUN pip install --no-cache-dir -r requirements.txt

ENV FLASK_APP=app.py
ENV FLASK_RUN_HOST=0.0.0.0
ENV FLASK_ENV=development

EXPOSE 5000

CMD ["flask", "run"]
