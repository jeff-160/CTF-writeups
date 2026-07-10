ARG PUBLIC_PLATFORM=linux/amd64
FROM --platform=$PUBLIC_PLATFORM python:3.11-slim-bookworm

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

WORKDIR /app
COPY requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir -r /app/requirements.txt

COPY app.py /app/app.py
COPY start.sh /start.sh
COPY flag /flag
COPY waf_guard /waf_guard

RUN chmod 755 /start.sh /app/app.py \
    && chmod 755 /waf_guard \
    && chmod 444 /flag

EXPOSE 8080
CMD ["/start.sh"]
