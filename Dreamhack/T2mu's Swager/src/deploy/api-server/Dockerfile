FROM python:3.10-slim-buster

ENV USER admin
RUN adduser --disabled-password -u 1337 $USER

WORKDIR /app
COPY . .
COPY --chown=root:root ./flag /

RUN pip install --upgrade pip && \
    pip install -r requirements.txt

RUN chmod +x ./run.sh
USER $USER
EXPOSE 8000

CMD ["./run.sh"]