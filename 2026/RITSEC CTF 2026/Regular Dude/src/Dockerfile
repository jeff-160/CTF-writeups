FROM python:3.10-slim

RUN pip install --no-cache-dir flask tensorflow-cpu

WORKDIR /app

COPY src/ .

ENV FLAG=REDACTED

EXPOSE 5000
CMD ["python", "main.py"]