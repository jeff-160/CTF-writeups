FROM node:16@sha256:496085d0cd8edf49c97ec86ac11bed85b6f965d9b29885887bb0edba26549b07

WORKDIR /usr/src/app
COPY ./deploy/src/ .
COPY ./deploy/flag /flag

RUN npm install
EXPOSE 3000
CMD [ "node", "app.js" ]
