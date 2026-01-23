FROM node:20-alpine

WORKDIR /app

COPY package*.json ./

RUN npm install

COPY ./src .

ENV FLAG "DH{sample_flag}"

EXPOSE 5000

CMD ["node", "app.js"]
