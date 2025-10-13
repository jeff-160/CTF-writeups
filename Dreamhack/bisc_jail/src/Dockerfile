FROM python:3.10-slim-buster
MAINTAINER n0paew

RUN apt-get update
RUN apt-get install -y xinetd socat
RUN pip install pyfiglet

RUN mkdir /home/bisc
RUN useradd -d /home/bisc bisc -s /bin/bash
RUN chown -R bisc:bisc /home/bisc
RUN chmod 750 /home/bisc
WORKDIR /home/bisc/

ADD ./bisc_jail.py /home/bisc/bisc_jail.py
ADD ./run.sh /run.sh
RUN chmod +x /home/bisc/bisc_jail.py
RUN chmod +x /run.sh

ADD ./flag /home/bisc/
RUN chown bisc:bisc /home/bisc/flag
RUN chmod 440 /home/bisc/flag

ADD ./bisc.xinetd /etc/xinetd/bisc
ADD ./start.sh /start.sh
RUN chmod +x /start.sh

CMD ["/usr/sbin/xinetd","-dontfork"]
