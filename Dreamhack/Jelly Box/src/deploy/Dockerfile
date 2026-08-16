FROM node:26.3.0-alpine

WORKDIR /app

COPY package.json ./
RUN npm install --omit=dev --no-audit --no-fund

COPY server.js ./
COPY flag.txt /flag.txt

EXPOSE 9797
CMD ["node", "server.js"]