FROM node:18-slim@sha256:781204f001403b0d27db2c49ab74ab1a5e867bd5e5c96ed5fcad6888e3b09f4a

WORKDIR /app

COPY deploy/package.json ./
COPY deploy/package-lock.json ./

RUN npm install

COPY deploy/prob.js ./
COPY flag.txt ./

EXPOSE 8000

CMD ["node", "prob.js"]