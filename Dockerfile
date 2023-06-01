FROM python:3.11.1-alpine3.17 as build
ENV PYTHONUNBUFFERED 1

RUN apk add --no-cache --virtual .build-deps \
    ca-certificates postgresql-dev linux-headers musl-dev \
    libffi-dev jpeg-dev zlib-dev

WORKDIR /usr/app/

RUN python -m venv /usr/app/venv
ENV PATH="/usr/app/venv/bin:$PATH"
COPY requirements.txt .
RUN pip install -r requirements.txt

RUN find /usr/local \
        \( -type d -a -name test -o -name tests \) \
        -o \( -type f -a -name '*.pyc' -o -name '*.pyo' \) \
        -exec rm -rf '{}' + \
    && runDeps="$( \
        scanelf --needed --nobanner --recursive /usr/local \
                | awk '{ gsub(/,/, "\nso:", $2); print "so:" $2 }' \
                | sort -u \
                | xargs -r apk info --installed \
                | sort -u \
    )" \
    && apk add --virtual .rundeps $runDeps \
    && apk del .build-deps


FROM python:3.11.1-alpine3.17@sha256:ab54613ad5bc67ae68a123837c7a4ac720ecd6ae81e002c796182074cda2f529
RUN addgroup -S python && adduser -S python -G python
USER python

WORKDIR /usr/app/
COPY --chown=python:python --from=build /usr/app/venv ./venv


# Copying requirements
COPY --chown=python:python . .

ENV PATH="/usr/app/venv/bin:$PATH"
RUN pip install -r requirements.txt

CMD ["./make.sh", "run"]

