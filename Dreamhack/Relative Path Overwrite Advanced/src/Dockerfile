FROM ubuntu:20.04

RUN sed -i 's/archive.ubuntu.com/mirror.kakao.com/g' /etc/apt/sources.list
RUN apt-get update -y
RUN apt-get upgrade -y

RUN apt-get install -y zip unzip
RUN apt-get install -y \
  php7.4 \
  php7.4-fpm

RUN apt-get install python3 apache2 libapache2-mod-php7.4 wget curl gnupg -y

RUN wget -q -O - https://dl-ssl.google.com/linux/linux_signing_key.pub | apt-key add - 
RUN echo "deb [arch=amd64] http://dl.google.com/linux/chrome/deb/ stable main" >> /etc/apt/sources.list.d/google.list
RUN apt-get update -y
RUN apt-get install -y python3-pip python-dev build-essential google-chrome-stable libnss3
RUN wget https://chromedriver.storage.googleapis.com/`curl -sS https://chromedriver.storage.googleapis.com/LATEST_RELEASE`/chromedriver_linux64.zip && unzip chromedriver_linux64.zip && rm chromedriver_linux64.zip

RUN pip3 install selenium

COPY ./deploy/src /var/www/html/
COPY ./deploy/flag.txt /flag.txt
COPY ./deploy/run-lamp.sh /usr/sbin/
COPY ./deploy/bot.py /
COPY ./deploy/000-default.conf /etc/apache2/sites-enabled/

RUN rm /var/www/html/index.html

RUN a2enmod rewrite
RUN chmod +x /usr/sbin/run-lamp.sh

EXPOSE 80

CMD ["/usr/sbin/run-lamp.sh"]
