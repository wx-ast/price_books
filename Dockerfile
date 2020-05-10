FROM registry.atyx.ru/baseimage:py38

ENV PYTHONUNBUFFERED 1

RUN apk update && \
    apk --no-cache add \
        python3 \
        uwsgi-python3 \
        mariadb-connector-c \
        freetype \
        lcms2 \
        libjpeg-turbo \
        libwebp \
        musl \
        py3-olefile \
        tiff \
        zlib \
        py3-pip && \
    pip3 install --upgrade pip

WORKDIR /srv

COPY poetry.lock .
COPY pyproject.toml .

RUN apk add --no-cache --virtual .build-deps \
        mariadb-dev \
        gcc \
        git \
        musl-dev \
        libffi-dev \
        jpeg-dev \
        zlib-dev \
        python3-dev && \
    pip3 install poetry && \
    poetry config virtualenvs.create false && \
    poetry install --no-dev && \
    apk del .build-deps

ENV PYTHONPATH="/srv:/usr/lib/python3.8:/usr/lib/python3.8/lib-dynload:/usr/lib/python3.8/site-packages"

CMD ["uwsgi", "--ini", "/conf/uwsgi.ini"]
ENTRYPOINT ["/init.sh"]
