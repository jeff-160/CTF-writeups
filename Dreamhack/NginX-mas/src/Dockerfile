FROM node:21-alpine3.17@sha256:a401c0e8f7c8ab151f056be73922a8c3663005e7872445d6e4eb3b12239f88c1

RUN apk update && apk add nginx

#only two vars are redacted
ENV FLAG=DH{REDACTED}
ENV DOMAIN=REDACTED.com

COPY default.conf /etc/nginx/http.d/
RUN sed -i "s/\$DOMAIN/$DOMAIN/g" /etc/nginx/http.d/default.conf

WORKDIR /app
COPY index.js /app
COPY package.json /app
RUN npm install

EXPOSE 80

CMD nginx && node index.js