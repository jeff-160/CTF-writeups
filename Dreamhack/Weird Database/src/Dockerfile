FROM node:18-alpine
COPY . /app
WORKDIR /app

RUN apk --no-cache add curl
RUN npm i

EXPOSE 3000

CMD ["node","index.js"]