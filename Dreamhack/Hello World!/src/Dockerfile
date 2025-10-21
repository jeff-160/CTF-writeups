FROM python:3.10-slim

RUN useradd -m dreamhack

COPY flag /flag

RUN chmod 111 /flag

WORKDIR /home/dreamhack

COPY src .

RUN chmod 666 hello.py

COPY requirements.txt ./

USER dreamhack

RUN pip install --user -r requirements.txt

CMD ["python3", "app.py"]