FROM python:3.13-slim

RUN apt-get update && apt-get install -y \
  xinetd \
  && rm -rf /var/lib/apt/lists/*

RUN mkdir -m 777 /app

COPY jail.py /app/
COPY flag.txt /app/
COPY jail.xinetd /etc/xinetd.d/jail

WORKDIR /app

EXPOSE 1337

CMD ["xinetd", "-dontfork"]
