FROM node:13-alpine

# dependencies for the newrelic agent
RUN apk add python make g++
WORKDIR /usr/src/app
COPY src/package.json .
RUN npm install
RUN cp /usr/src/app/node_modules/newrelic/newrelic.js .

FROM node:13-alpine
COPY --from=0 /usr/src/app /usr/src/app
WORKDIR /usr/src/app
COPY src .
CMD [ "node", "app.js" ]
