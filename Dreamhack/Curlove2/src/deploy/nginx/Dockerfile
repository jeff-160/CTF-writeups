FROM nginx:latest

ENV PORT 8001
COPY ./nginx.conf /etc/nginx/nginx.conf

COPY entrypoint.sh /entrypoint.sh

RUN chmod 700 /entrypoint.sh
RUN chmod +x /entrypoint.sh

EXPOSE $PORT
ENTRYPOINT ["/entrypoint.sh"]
CMD ["nginx", "-g", "daemon off;"]