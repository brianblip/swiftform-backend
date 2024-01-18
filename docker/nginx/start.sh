#!/bin/bash
envsubst '$FLASK_SERVER_ADDR' < /etc/nginx/fpm.tmpl > /etc/nginx/conf.d/default.conf
exec nginx -g "daemon off;"