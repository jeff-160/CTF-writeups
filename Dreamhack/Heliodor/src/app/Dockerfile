# FROM node:16-alpine
FROM node@sha256:1908564153449b1c46b329e6ce2307e226bc566294f822f11c5a8bcef4eeaad7

ENV USER heliodor
ENV PORT 58283
ENV NODE_ENV production
ENV FLAG GoN{sample_flag}

# Change tmp permissions
RUN chmod 1733 /tmp /var/tmp /dev/shm

# Add user
RUN adduser -D -g "" $USER

# Add files
COPY --chown=root:root heliodor /heliodor

WORKDIR /heliodor
RUN npm install

# Add initial empty jsonfs
USER $USER
RUN mkdir /tmp/jsonfs

CMD ["npm", "start"]
EXPOSE $PORT
