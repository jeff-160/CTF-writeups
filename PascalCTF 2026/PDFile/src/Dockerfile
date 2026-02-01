FROM python:3.13

ARG FLAG

WORKDIR /app

COPY requirements.txt .
RUN apt-get update && apt-get install -y libxml2-dev libxslt-dev gcc zlib1g-dev
RUN pip install --no-cache-dir --no-binary lxml -r requirements.txt

COPY . .
RUN echo "$FLAG" > /app/flag.txt
RUN chmod 400 /app/flag.txt

RUN mkdir -p uploads && chmod 777 uploads

RUN useradd -m -u 1000 appuser && chown -R appuser:appuser /app
USER appuser

EXPOSE 5000

CMD ["gunicorn", "--bind", "0.0.0.0:5000", "--workers", "2", "app:app"]
