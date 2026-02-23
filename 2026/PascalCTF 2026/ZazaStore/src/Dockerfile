FROM node:24-alpine

WORKDIR /app

COPY app/*.json .
RUN npm install

COPY app/ .

ENTRYPOINT ["npm", "start"]