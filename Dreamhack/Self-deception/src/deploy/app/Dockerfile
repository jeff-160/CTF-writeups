FROM node:20.5

ENV USER developer
ENV PORT 3000

RUN adduser --disabled-password $USER

RUN apt-get update -y && apt-get install -y curl

WORKDIR /app

COPY package*.json ./

RUN npm install

COPY . .
RUN chmod +x entrypoint.sh
USER $USER
EXPOSE $PORT

ENTRYPOINT ["./entrypoint.sh"]
CMD ["node", "app.js"]