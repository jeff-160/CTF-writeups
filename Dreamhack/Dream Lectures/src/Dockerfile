FROM python:3

ARG DEBIAN_FRONTEND=noninteractive

ENV TZ=Asia/Seoul
ENV user login_page
ENV port 8000

RUN wget -q -O - https://dl-ssl.google.com/linux/linux_signing_key.pub | apt-key add - && echo 'deb [arch=amd64] http://dl.google.com/linux/chrome/deb/ stable main' | tee /etc/apt/sources.list.d/google-chrome.list

RUN apt-get update -y && apt-get install -y \
        google-chrome-stable \
        mariadb-common \
        mariadb-server \
        mariadb-client \
        tzdata

RUN ln -sf /usr/share/zoneinfo/Asia/Seoul /etc/localtime
RUN dpkg-reconfigure tzdata

RUN wget https://chromedriver.storage.googleapis.com/`curl -sS https://chromedriver.storage.googleapis.com/LATEST_RELEASE`/chromedriver_linux64.zip && unzip chromedriver_linux64.zip && rm chromedriver_linux64.zip

RUN pip install --upgrade pip

RUN adduser $user
ADD ./deploy/app /app
WORKDIR /app
RUN pip install -r requirements.txt
RUN chmod +x run.sh

RUN /bin/bash -c "/usr/bin/mysqld_safe &" && \
  sleep 5 && \
  mysql -uroot < /app/init.sql
RUN rm /app/init.sql

EXPOSE $port

CMD ["./run.sh"]
