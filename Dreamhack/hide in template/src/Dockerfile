FROM ubuntu:22.04

RUN apt-get update && \
    DEBIAN_FRONTEND="noninteractive" apt-get install -y python3 python3-pip python3-wheel net-tools curl libglib2.0-0 libnss3 libgconf-2-4 libfontconfig1 && python3 -m pip install --upgrade pip
RUN pip3 install --ignore-installed Flask flask-login uWSGI flask-session
RUN rm -rf /var/lib/apt/lists/*

RUN useradd -ms /bin/bash ctf

COPY *flag.txt /

WORKDIR /app

COPY deploy .

EXPOSE 5000

COPY --chown=root entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh
ENTRYPOINT ["/entrypoint.sh"]
