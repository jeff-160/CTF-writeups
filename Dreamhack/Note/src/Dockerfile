FROM node:18

WORKDIR /app
COPY . /app
COPY ./flag.txt /flag.txt
RUN npm install
ENV port 3000

RUN useradd todo
RUN chown -R todo:todo /app
RUN chmod 644 /flag.txt
USER todo

CMD ["node", "server.js"]