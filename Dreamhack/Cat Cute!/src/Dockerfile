FROM node:18-alpine

COPY ./src/ /app/

RUN apk update && apk upgrade
RUN apk add chromium 

WORKDIR /app
RUN echo "bisc2023{FAKE_FLAG}" > flag.txt

RUN npm install
EXPOSE 3000
CMD ["node","app.js"]
