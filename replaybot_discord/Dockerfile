FROM node:13-alpine
WORKDIR /usr/src/app
COPY src/package.json .
RUN npm install
COPY src .
CMD [ "node", "app.js" ]