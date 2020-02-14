#!/bin/sh
# Get latest s2protocol on startup
pip install --upgrade s2protocol
nginx
uwsgi --lazy --ini /config/uwsgi.ini --py-autoreload 1