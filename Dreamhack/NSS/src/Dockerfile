FROM node:current-alpine3.15

WORKDIR /usr/src/app

COPY package*.json ./

RUN npm install
RUN npm install -g npm@8.5.4

COPY . .

EXPOSE 80

CMD [ "node", "main.js" ]