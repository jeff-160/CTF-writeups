FROM python:3.9

ENV env "production"

ENV APP_USER "dreamhack"
ENV APP_PORT 5000
ENV FLAG "DH{FLAG}"
ENV FLAG_SCHOOL "드림대학교"

RUN adduser --disabled-password $APP_USER

COPY --chown=$APP_USER ./app /app
WORKDIR /app

RUN pip install -r requirements.txt
RUN sed -i.bak '143,146d' /usr/local/lib/python3.9/site-packages/jwt/algorithms.py

USER $APP_USER
EXPOSE $APP_PORT

CMD ["sh", "-c", "gunicorn -b 0.0.0.0:$APP_PORT wsgi:app -k gevent"]
