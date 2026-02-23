FROM ubuntu:20.04

ENV DEBIAN_FRONTEND=noninteractive
ENV USER=user
ENV FLAG=flag.txt
ENV PROB=server.py
ENV PORT=31006
ENV TIMEOUT=60

RUN apt-get update && apt-get upgrade -y
RUN apt-get install nodejs npm tzdata python3 python3-pip python3-dev build-essential -y

# For user create.
# For user create.
# For user create.
# For user create.
# For user create.
# For user create.
RUN mkdir /home/$USER

COPY $FLAG /home/$USER/$FLAG
COPY $PROB /home/$USER/$PROB

RUN pip3 install --no-cache-dir \
    flask \
    lxml \
    opencv-python \
    numpy \
    hexdump

RUN chown -R root:$USER /home/$USER && \
    chmod 750 /home/$USER && \
    chmod 440 /home/$USER/$FLAG && \
    chmod 750 /home/$USER/$PROB

RUN chmod 755 /bin/sh /bin/bash /usr/bin/python3

WORKDIR /home/$USER
USER $USER

CMD python3 /home/$USER/$PROB
