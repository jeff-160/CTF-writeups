FROM node:20-bookworm

WORKDIR /app

COPY app/package.json app/package-lock.json app/bot-requirements.txt ./

RUN npm install --omit=dev

RUN apt-get update \
    && apt-get install -y --no-install-recommends \
        python3 \
        python3-venv \
        ca-certificates \
        wget \
        unzip \
    && wget -O /tmp/google-chrome-stable.deb https://mirror.cs.uchicago.edu/google-chrome/pool/main/g/google-chrome-stable/google-chrome-stable_141.0.7390.54-1_amd64.deb \
    && apt-get install -y /tmp/google-chrome-stable.deb \
    && rm -f /tmp/google-chrome-stable.deb \
    && wget -O /tmp/chromedriver.zip https://storage.googleapis.com/chrome-for-testing-public/141.0.7390.54/linux64/chromedriver-linux64.zip \
    && unzip /tmp/chromedriver.zip -d /tmp/chromedriver-unpack \
    && mv /tmp/chromedriver-unpack/chromedriver-linux64/chromedriver /usr/local/bin/chromedriver \
    && chmod +x /usr/local/bin/chromedriver \
    && rm -rf /tmp/chromedriver.zip /tmp/chromedriver-unpack \
    && ln -sf /usr/bin/python3 /usr/local/bin/python \
    && python3 -m venv /opt/bot-venv \
    && /opt/bot-venv/bin/pip install --no-cache-dir -r bot-requirements.txt \
    && rm -rf /var/lib/apt/lists/*

COPY app/ ./
COPY flag /flag

RUN chmod 444 /flag

ENV NODE_ENV=production
ENV PORT=3000
ENV TIMEOUT=60000
ENV DRIVER=/usr/local/bin/chromedriver
ENV CHROME=/usr/bin/google-chrome
ENV PYTHON=/opt/bot-venv/bin/python

EXPOSE 3000

CMD ["node", "server.js"]
