FROM python:3.11-slim

RUN apt update && apt install -y git
RUN apt-get update -y && apt-get install -y python3-pip build-essential

RUN pip install --upgrade pip

COPY . /app
WORKDIR /app

RUN echo "DH{this_is_not_real_flag}" > flag
RUN pip install -r requirements.txt

EXPOSE 9000

CMD ["python3", "app.py"]