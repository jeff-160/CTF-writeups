FROM python:3.14-slim@sha256:2751cbe93751f0147bc1584be957c6dd4c5f977c3d4e0396b56456a9fd4ed137

WORKDIR /app

RUN apt-get update && apt-get install -y mariadb-client
RUN pip install flask

COPY ./src /app

COPY ./flag.txt /flag_**redacted**.txt

EXPOSE 8080

CMD ["python", "app.py"]
