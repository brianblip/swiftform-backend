FROM python:3.11.7-alpine

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV PYTHONPATH=/usr/lib/python3.11/site-packages/:/home/sf/app/swiftform/

RUN apk update \
    && apk add curl \
    && apk add git \
    && apk add py3-gunicorn \
    && apk add py3-setuptools \
    && apk add py3-flask-sqlalchemy \
    && apk add py3-alembic \
    && apk add py3-flask \
    && apk add py3-dotenv \
    && apk add py3-psycopg2 \
    && apk add py3-flask-cors

# Install flask-jwt-extended
RUN git clone https://github.com/vimalloc/flask-jwt-extended.git \
    && cd flask-jwt-extended \
    && python setup.py install --prefix /usr

# Install flask-alembic
RUN git clone https://github.com/davidism/flask-alembic.git \
    && cd flask-alembic \
    && pip install --upgrade -e . --target /usr/lib/python3.11/site-packages

# Install openai
RUN git clone https://github.com/openai/openai-python.git \
    && cd openai-python \
    && pip install -e . --target /usr/lib/python3.11/site-packages

RUN adduser -D sf
RUN mkdir -p /home/sf/app && chown -R sf:sf /home/sf/app
RUN mkdir -p /var/log/flask-app && touch /var/log/flask-app/flask-app.err.log && touch /var/log/flask-app/flask-app.out.log
RUN chown -R sf:sf /var/log/flask-app

WORKDIR /home/sf/app
USER sf

COPY --chown=sf:sf . .

EXPOSE 8000

RUN chmod +x /home/sf/app/docker/python/start.sh

ENTRYPOINT [ "/bin/sh", "/home/sf/app/docker/python/start.sh" ]