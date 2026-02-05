FROM node:20-alpine@sha256:c13b26e7e602ef2f1074aef304ce6e9b7dd284c419b35d89fcf3cc8e44a8def9

WORKDIR /app

COPY ./deploy .

RUN npm ci
RUN npm install -g typescript
RUN npm run build

EXPOSE 3000

CMD ["npm", "start"]