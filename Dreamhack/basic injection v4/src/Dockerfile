FROM node:18

WORKDIR /app

RUN npm init -y && \
    npm install express@4.18.2 \
                express-session@1.17.3 \
                redis@3.1.2 \
                connect-redis@6.1.3 \
                dot@1.1.3 \
                qs@6.5.2

RUN apt-get update && \
    apt-get install -y redis-server && \
    rm -rf /var/lib/apt/lists/*

COPY app.js .
COPY flag /

RUN echo '#!/bin/bash\n\
redis-server --daemonize yes\n\
sleep 2\n\
node app.js' > /app/start.sh && \
    chmod +x /app/start.sh

EXPOSE 5000

CMD ["/app/start.sh"]