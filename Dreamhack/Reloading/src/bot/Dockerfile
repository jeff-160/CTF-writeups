FROM python@sha256:78832558cefff2e881078ac5b241fa9b25fd9c47aefdfb452a788383d78a49fd

ENV USER=dreamhack
RUN adduser --disabled-password -u 1337 $USER

RUN apt-get update -y && apt-get install -y python3-pip build-essential wget curl unzip

RUN apt-get update \
    && apt-get install -y --no-install-recommends \
        gnupg \
        ca-certificates \
    && wget -q -O - https://dl.google.com/linux/linux_signing_key.pub | apt-key add - \
    && sh -c 'echo "deb [arch=amd64] http://dl.google.com/linux/chrome/deb/ stable main" >> /etc/apt/sources.list.d/google-chrome.list' \
    && apt-get update \
    && apt-get install -y \
        google-chrome-stable \
    && rm -rf /var/lib/apt/lists/* \
    && apt-get clean

## chromedriver
RUN wget https://storage.googleapis.com/chrome-for-testing-public/`curl -sS https://googlechromelabs.github.io/chrome-for-testing/LATEST_RELEASE_STABLE`/linux64/chromedriver-linux64.zip \
    && unzip chromedriver-linux64.zip \
    && rm chromedriver-linux64.zip

WORKDIR /app
COPY . /app

RUN chmod 777 /app
RUN chmod 555 bot.py
RUN rm -rf Dockerfile


COPY requirements.txt /app
RUN pip3 install -r requirements.txt

CMD ["python3","bot.py"]
