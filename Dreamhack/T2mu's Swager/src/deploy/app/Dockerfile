FROM node:20.5.1-slim

ENV USER=app
ENV PORT=3000
RUN adduser --disabled-password -u 1337 $USER

RUN apt-get update \
&& apt-get install -y curl

WORKDIR /app
COPY . .
RUN npm install

EXPOSE $PORT
CMD ["node","app.js"]