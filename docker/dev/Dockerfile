FROM python:3.12

ARG ENVIRONMENT

ENV HOME=/home/ \
    APP_HOME=/home/app \
    PYTHONPATH="$PYTHONPATH:$APP_HOME" \
    PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

RUN mkdir -p $APP_HOME \
    && groupadd -r referralapi \
    && useradd -r -g referralapi referralapi

WORKDIR $HOME

COPY ../../requirements.txt .

RUN pip install --upgrade pip \
    && pip install -r requirements.txt

COPY ../../app ./app
ADD ../../alembic.ini .
COPY ../../scripts/wait-for-it.sh ./scripts/wait-for-it.sh

RUN chown -R referralapi:referralapi .

USER referralapi