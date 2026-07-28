FROM python:3.14.0rc2-slim-bookworm

WORKDIR /app
COPY deploy/ /app/

RUN pip install flask
RUN useradd -m user
RUN chown -R user:user /app

USER user
EXPOSE 3000

CMD ["python", "app.py"]