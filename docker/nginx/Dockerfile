FROM nginx:1.25.3-alpine

RUN apk update \
    apk add bash

RUN rm -f /etc/nginx/conf.d/default.conf
RUN rm -f /etc/nginx/nginx.conf

COPY --chown=nginx:nginx ./docker/nginx/nginx.conf /etc/nginx/nginx.conf
COPY --chown=nginx:nginx ./docker/nginx/default.conf /etc/nginx/fpm.tmpl
COPY --chown=nginx:nginx ./docker/nginx/start.sh /home/sf/app/start.sh

EXPOSE 80

ENTRYPOINT [ "/bin/sh", "/home/sf/app/start.sh" ]