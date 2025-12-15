FROM node:18-alpine

WORKDIR /app

COPY package.json .
RUN npm config set registry https://registry.npmjs.org/ && npm install
RUN npm install
RUN apk add --no-cache python3
COPY server.js .
COPY static/style.css static/
COPY views/error.ejs views/
COPY views/index.ejs views/
COPY views/result.ejs views/
COPY flag /
EXPOSE 5000

CMD ["npm", "start"]