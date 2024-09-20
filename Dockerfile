FROM python:2.7-alpine AS base

RUN	apk update && apk add --no-cache \
	libxslt-dev libxml2-dev build-base \
	tiff-dev jpeg-dev openjpeg-dev zlib-dev freetype-dev lcms2-dev \
	libwebp-dev tcl-dev tk-dev harfbuzz-dev fribidi-dev \
	libxcb-dev libpng-dev \
	postgresql-dev
COPY requirements.txt requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

WORKDIR /app


FROM base AS dev



FROM base AS prod

RUN pip install --no-cache-dir gunicorn psycopg2-binary

COPY . /app
