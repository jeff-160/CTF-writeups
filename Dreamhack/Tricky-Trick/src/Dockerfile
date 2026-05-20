FROM python:3.8.20-slim-bullseye

# ENV
ENV user restriction
ENV port 8000

RUN apt-get update -y && apt-get install -y build-essential wget curl unzip libxml2-dev libxslt1-dev zlib1g-dev

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

WORKDIR /
RUN wget https://files.pythonhosted.org/packages/source/l/lxml/lxml-4.6.0.tar.gz
RUN tar -xvzf lxml-4.6.0.tar.gz
RUN cd lxml-4.6.0
# RUN git clone https://github.com/lxml/lxml.git
WORKDIR /lxml-4.6.0

# RUN git checkout lxml-4.6.0
RUN python setup.py build
RUN python setup.py install

# SET challenges
RUN adduser -u 1337 $user
ADD ./deploy /app
WORKDIR /app
RUN pip3 install -r requirements.txt

RUN chown root:$user /app/flag.txt

# RUN
USER $user
EXPOSE $port

ENTRYPOINT ["python3"]
CMD ["app.py"]

