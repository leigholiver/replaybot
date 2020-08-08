FROM alpine:3.11
RUN apk add py-pip g++ linux-headers python-dev git
WORKDIR /app
COPY ./config/requirements.txt /app
RUN pip install -r ./requirements.txt

FROM alpine:3.11
RUN apk add nginx py-pip
COPY --from=0 /usr/lib/python2.7/site-packages /usr/lib/python2.7/site-packages
COPY --from=0 /usr/bin/uwsgi /usr/bin/uwsgi

COPY config /config
COPY config/nginx.conf /etc/nginx/nginx.conf

RUN adduser -D -g 'www' www
RUN chmod +x /config/start.sh

WORKDIR /app
COPY src /app

ENTRYPOINT ["/config/start.sh"]
