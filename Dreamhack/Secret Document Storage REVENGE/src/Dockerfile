FROM ubuntu:22.04@sha256:2b7412e6465c3c7fc5bb21d3e6f1917c167358449fecac8176c6e496e5c1f05f

ENV DEBIAN_FRONTEND=noninteractive

RUN apt update && apt install -y software-properties-common
RUN add-apt-repository ppa:ondrej/php && \
    apt update && \
    apt install -y php7.4 mysql-server apache2
RUN apt install -y php7.4-mysqli
RUN apt install php7.4-curl



COPY ./readflag /readflag

RUN chmod 700 /readflag
RUN rm -rf /var/www/html/*


COPY ./src/ /var/www/html/
COPY ./init.sql /docker-entrypoint-initdb.d/

RUN mkdir -p /var/www/html/uploads
RUN chmod 777 /var/www/html/uploads

# 권한 상승 벡터 제외

EXPOSE 80

CMD service mysql start && \
    mysql -u root < /docker-entrypoint-initdb.d/init.sql && \
    service apache2 start && \
    rm -rf /docker-entrypoint-initdb.d && \
    tail -f /dev/null
