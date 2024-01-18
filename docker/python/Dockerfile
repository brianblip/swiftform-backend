FROM python:3.12.1-alpine

RUN pip install --upgrade pip

RUN apk update \
    apk add curl

RUN adduser -D sf
RUN mkdir -p /home/sf/app && chown -R sf:sf /home/sf/app
RUN mkdir -p /var/log/flask-app && touch /var/log/flask-app/flask-app.err.log && touch /var/log/flask-app/flask-app.out.log
RUN chown -R sf:sf /var/log/flask-app

WORKDIR /home/sf/app
USER sf

COPY --chown=sf:sf . .

ENV VIRTUAL_ENV=/home/sf/.venv

RUN python -m venv $VIRTUAL_ENV
ENV PATH="$VIRTUAL_ENV/bin:$PATH"
RUN export FLASK_APP=app.py
RUN pip install -r requirements.txt

EXPOSE 8000

CMD ["gunicorn", "-w", "3", "-t", "60", "-b", "0.0.0.0:8000", "swiftform.app:create_app()"]