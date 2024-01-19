#!/bin/sh

gunicorn \
    -w 3 \
    -t 60 \
    -b $FLASK_HOST:$FLASK_PORT \
    $FLASK_APP