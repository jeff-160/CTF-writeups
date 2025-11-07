FROM python:3.9-slim

WORKDIR /app

COPY . /app

RUN echo "pokactf2024{**flag**}" > /flag

RUN pip install Flask requests

RUN rm -f /usr/bin/login /bin/login 

CMD ["python", "app.py"]
