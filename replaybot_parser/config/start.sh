#!/bin/sh
nginx
newrelic-admin generate-config $NEWRELIC_LICENSE_KEY newrelic.ini
sed -i 's/app_name\ =\ .*/app_name\ =\ replaybot_parser/' newrelic.ini
echo "log_file = stderr" >> newrelic.ini
NEW_RELIC_CONFIG_FILE=newrelic.ini newrelic-admin run-program uwsgi --lazy --ini /config/uwsgi.ini --py-autoreload 1
