FROM node:20.7.0-alpine3.17@sha256:2d808029dd5a1e6a606c06a3c78fbb770f53d2603827e7fcfbc7878848749152

ENV USER ctf
ENV PORT 8080
ENV NODE_ENV production

# Change tmp permissions
RUN chmod 1733 /tmp /var/tmp /dev/shm

# Add user
RUN adduser -D -g "" $USER

# Add files
COPY --chown=root:ctf server.js flag /
RUN chmod 440 /flag /server.js \
 && mv /flag /flag_$(md5sum /flag | awk '{print $1}')

USER $USER
EXPOSE $PORT
CMD ["node", "/server.js"]
