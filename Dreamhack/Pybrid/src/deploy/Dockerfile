FROM python:3.9-slim

WORKDIR /usr/src/app

COPY . .

RUN pip install flask

COPY flag.txt /flag.txt

CMD ["python", "app.py"]
