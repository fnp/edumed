FROM turicas/python:2.7-slim-bookworm AS base

RUN apt-get update && apt-get install -y \
    libxslt-dev libxml2-dev build-essential \
    libtiff5-dev libjpeg62-turbo-dev libopenjp2-7-dev zlib1g-dev \
    libfreetype6-dev liblcms2-dev libwebp-dev tcl8.6-dev tk8.6-dev python3-tk \
    libharfbuzz-dev libfribidi-dev libxcb1-dev \
    libpq-dev \
    ruby-sass \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

WORKDIR /app/src


FROM base AS dev



FROM base AS prod

RUN pip install --no-cache-dir gunicorn psycopg2-binary

COPY src /app/src/
