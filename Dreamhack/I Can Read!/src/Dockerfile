# FROM ubuntu:20.04
FROM python:3.8

# RUN apt update && apt install -y python3.8
# RUN apt install python3-pip -y
RUN apt install curl -y
RUN pip3 install flask

WORKDIR /var/www/
COPY main ./main/
COPY admin ./admin/
RUN chmod 755 /var/www/
COPY flag /
RUN chmod 700 /flag
ADD run.sh /run.sh
RUN useradd user
CMD ["/run.sh"]

EXPOSE 5000