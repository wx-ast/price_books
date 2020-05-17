FROM registry.atyx.ru/baseimage:py38

ENV PYTHONUNBUFFERED 1

RUN apk update && \
    apk --no-cache add \
        python3 \
        uwsgi-python3 \
        mariadb-connector-c \
        musl \
        py3-pip && \
    pip3 install --upgrade pip

WORKDIR /srv

COPY poetry.lock .
COPY pyproject.toml .

ARG POETRY_INSTALL_OPTIONS

RUN apk add --no-cache --virtual .build-deps \
        mariadb-dev \
        gcc \
        git \
        musl-dev \
        libffi-dev \
        python3-dev && \
    pip3 install poetry && \
    poetry config virtualenvs.create false && \
    poetry install $POETRY_INSTALL_OPTIONS && \
    apk del .build-deps

ENV PYTHONPATH="/srv:/usr/lib/python3.8:/usr/lib/python3.8/lib-dynload:/usr/lib/python3.8/site-packages"

CMD ["uwsgi", "--ini", "/conf/uwsgi.ini"]
ENTRYPOINT ["/init.sh"]
