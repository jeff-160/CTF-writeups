FROM python:3.10-slim-buster

ENV USER dreamhack
ENV PORT 8080
RUN adduser --disabled-password -u 1337 $USER

WORKDIR /app
COPY . .

RUN chown -R root:$USER /app
RUN chmod 775 /app

RUN pip install --no-cache-dir -r requirements.txt

EXPOSE $PORT
USER $USER
CMD ["python3", "app.py"]
