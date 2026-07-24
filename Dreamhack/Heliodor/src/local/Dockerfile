# FROM python:3.10-alpine
FROM python@sha256:0c46c7f15ee201a2e2dc3579dbc302f989a20b1283e67f884941e071372eb2cc

ENV USER local
ENV PORT 2222

RUN apk add --no-cache socat bash \
 && pip install requests

# Change tmp permissions
RUN chmod 1733 /tmp /var/tmp /dev/shm

# Add user
RUN adduser -D -g "" $USER \
 && chown -R root:root /home/$USER

WORKDIR /tmp
CMD socat TCP-LISTEN:$PORT,reuseaddr,fork EXEC:'bash -li',pty,stderr,setsid,sigint,sane,su=$USER
EXPOSE $PORT
