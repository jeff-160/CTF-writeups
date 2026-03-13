FROM python:3.9

ENV user chall

RUN pip install --upgrade pip
RUN pip install fastapi==0.105.0 uvicorn==0.24.0.post1 Jinja2==3.1.2 httptools==0.6.1
RUN pip install starlette==0.32.0

RUN adduser --disabled-password $user
WORKDIR /app/
ADD ./app /app

USER $user
EXPOSE 8000

CMD uvicorn --host=0.0.0.0 --port 8000 app:app