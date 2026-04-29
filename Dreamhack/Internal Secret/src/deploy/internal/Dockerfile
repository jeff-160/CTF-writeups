FROM python:3.11-slim
COPY flag /flag
WORKDIR /app
COPY requirements.txt .
COPY internal.py .
RUN pip install --no-cache-dir -r requirements.txt
CMD ["python", "internal.py"]
