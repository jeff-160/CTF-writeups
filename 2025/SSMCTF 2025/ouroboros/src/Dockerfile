FROM --platform=linux/amd64 python:3.11-slim-bookworm

WORKDIR /challf

COPY ouroboros.py .
COPY ynetd .
COPY flag .

RUN chmod +x ouroboros.py
RUN chmod +x ynetd

EXPOSE 8000

RUN adduser ouro
USER ouro

CMD ./ynetd -p 8000 "python3 ouroboros.py"
