FROM python:3.10-slim-buster


WORKDIR /app
COPY . /app

RUN chmod 777 /app
RUN chmod 555 app.py
RUN rm -rf Dockerfile
RUN rm -rf flag.txt

RUN groupadd --system dothack && \
    useradd --system --gid dothack dothack

COPY requirements.txt /app
RUN pip3 install -r requirements.txt

USER dothack

RUN rm -rf /tmp/*

CMD ["python3","app.py"]