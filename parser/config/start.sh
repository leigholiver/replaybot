#!/bin/sh
nginx
newrelic-admin generate-config $NEW_RELIC_LICENSE_KEY newrelic.ini
sed -i "s/app_name\\ =\\ .*/app_name\\ =\\ $NEW_RELIC_APP_NAME/" newrelic.ini
echo "log_file = stderr" >> newrelic.ini
NEW_RELIC_CONFIG_FILE=newrelic.ini newrelic-admin run-program uwsgi --lazy --ini /config/uwsgi.ini --py-autoreload 1
