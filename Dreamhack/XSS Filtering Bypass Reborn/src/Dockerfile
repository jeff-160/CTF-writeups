# 최신 Python slim 이미지 사용
FROM python:3.13-slim

# 환경변수
ENV USER=rootsquare

# 필수 패키지 설치
RUN apt-get update -y && \
    apt-get install -y --no-install-recommends \
        build-essential \
        wget \
        curl \
        unzip \
        libxml2-dev \
        libxslt1-dev \
        zlib1g-dev \
        gnupg \
        ca-certificates && \
    rm -rf /var/lib/apt/lists/*

# Google Chrome GPG key 가져오기 (apt-key 대신 keyrings 사용)
RUN curl -fsSL https://dl.google.com/linux/linux_signing_key.pub \
    | gpg --dearmor -o /usr/share/keyrings/google-linux.gpg

# Chrome repository 등록 (signed-by 옵션 사용)
RUN echo "deb [arch=amd64 signed-by=/usr/share/keyrings/google-linux.gpg] http://dl.google.com/linux/chrome/deb/ stable main" \
    > /etc/apt/sources.list.d/google-chrome.list

# Chrome 설치
RUN apt-get update && \
    apt-get install -y google-chrome-stable && \
    rm -rf /var/lib/apt/lists/* && \
    apt-get clean

# 최신 ChromeDriver 다운로드 및 설치
RUN set -eux; \
    LATEST=$(curl -sS https://googlechromelabs.github.io/chrome-for-testing/LATEST_RELEASE_STABLE); \
    wget -q https://storage.googleapis.com/chrome-for-testing-public/${LATEST}/linux64/chromedriver-linux64.zip; \
    unzip -o chromedriver-linux64.zip; \
    mv chromedriver-linux64/chromedriver /usr/local/bin/; \
    chmod +x /usr/local/bin/chromedriver; \
    rm -rf chromedriver-linux64.zip chromedriver-linux64

RUN ln -s /usr/local/bin/chromedriver /chromedriver || true

# SET challenges
RUN adduser $USER
COPY ./deploy /app
WORKDIR /app
RUN pip3 install -r requirements.txt

RUN chown root:$USER /app/flag.txt

# RUN
USER $USER

EXPOSE 8000

CMD ["python", "app.py"]