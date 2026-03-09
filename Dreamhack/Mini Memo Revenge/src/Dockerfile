FROM gcc:15.2.0 AS builder

COPY ./flag.txt /flag.txt
COPY ./readflag.c /readflag.c
RUN gcc -o /readflag /readflag.c -static -O2

FROM python:3.9-slim AS production

RUN groupadd -r flag && useradd -r -g flag flag
COPY --from=builder --chown=flag:flag --chmod=400 /flag.txt /flag.txt
COPY --from=builder --chown=flag:flag --chmod=4711 /readflag /readflag

WORKDIR /app

COPY ./src/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY ./src .

RUN mkdir -p templates memo_templates

RUN groupadd -r appuser && useradd -r -g appuser appuser
RUN chown -R appuser:appuser /app

USER appuser
EXPOSE 5000

CMD ["python", "app.py"]
