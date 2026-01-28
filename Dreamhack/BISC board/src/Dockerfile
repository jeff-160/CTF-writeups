FROM node

RUN mkdir -p /app
RUN echo 'BISC2023{fakeflag}' > /flag.txt

WORKDIR /app

COPY ./ /app

RUN npm install

EXPOSE 80

CMD ["npm","start"]
