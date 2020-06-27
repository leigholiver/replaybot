#!/bin/sh
nginx
uwsgi --lazy --ini /config/uwsgi.ini --py-autoreload 1