FROM python:3.13.4-alpine

WORKDIR /app

RUN pip install flask

ADD ./deploy /chall
WORKDIR /chall

EXPOSE 5000

CMD ["python", "app.py"]