FROM alpine:3.11
RUN apk add py-pip g++ linux-headers python-dev
WORKDIR /app
COPY ./config/requirements.txt /app
RUN pip install -r ./requirements.txt

FROM alpine:3.11
RUN apk add nginx py-pip
COPY --from=0 /usr/lib/python2.7/site-packages /usr/lib/python2.7/site-packages
COPY --from=0 /usr/bin/uwsgi /usr/bin/uwsgi

RUN apk add py-pip
RUN pip install newrelic

COPY config /config
RUN chmod +x /config/start.sh

COPY config/nginx.conf /etc/nginx/nginx.conf
RUN adduser -D -g 'www' www

WORKDIR /app
COPY src /app

ENTRYPOINT ["/config/start.sh"]
