FROM python:3.11-slim

RUN apt-get update && apt-get install -y python3-pip

RUN pip install --upgrade pip

COPY . /app
WORKDIR /app

RUN gcc /app/flag.c -o /flag && chmod 111 /flag && rm /app/flag.c
RUN pip install -r requirements.txt

EXPOSE 9000

CMD ["python3", "app.py"]