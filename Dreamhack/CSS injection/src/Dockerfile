FROM python:3.10-slim-buster
# FROM tiangolo/uwsgi-nginx-flask:python3.10

# ENV
ENV user dreamhack
ENV port 8000

RUN apt-get update && apt-get install -y python3-pip wget curl unzip gnupg2

## chrome
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

# SET challenges
RUN adduser $user
ADD ./deploy /app
WORKDIR /app
RUN pip3 install -r requirements.txt
RUN ls -al

RUN chown root:$user /app/flag.txt

# RUN
EXPOSE $port

ENTRYPOINT ["python3"]
CMD ["main.py"]