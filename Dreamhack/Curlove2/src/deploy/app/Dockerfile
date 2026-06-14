FROM python:3.10-slim-buster

ENV USER dreamhack
ENV PORT 8002
RUN adduser --disabled-password -u 1337 $USER

RUN apt-get update -y && apt-get install -y python3-pip build-essential wget unzip sqlite3 make libssl-dev
RUN wget https://curl.se/download/curl-8.4.0.tar.gz && \
    tar -xvzf curl-8.4.0.tar.gz && \
    cd curl-8.4.0 && \
    ./configure --with-openssl --with-libcurl=/usr/local/lib && \
    make && \
    make install && \
    ldconfig

ENV LD_LIBRARY_PATH /usr/local/lib:$LD_LIBRARY_PATH

RUN pip install --upgrade pip

WORKDIR /app
COPY ./templates ./templates
COPY ./app.py .
COPY ./requirements.txt .
COPY ./schema.sql .
COPY ./flag.txt .
COPY ./utils.py .


RUN chown -R root:$USER /app
RUN chmod 775 /app
RUN pip install -r /app/requirements.txt

EXPOSE $PORT
USER $USER
CMD ["python3","app.py"]