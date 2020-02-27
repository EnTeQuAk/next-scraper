FROM python:3.8-slim-buster

RUN apt-get update && apt-get install -y \
    gcc \
    build-essential \
    libpq-dev

ENV PIP_BUILD=/deps/build/
ENV PIP_CACHE_DIR=/deps/cache/
ENV PIP_SRC=/deps/src/

# supervisord to run services, watchdog for celery autoreload
# and ipython for easier debugging
RUN pip install supervisor
RUN pip install watchdog[watchmedo]
RUN pip install ipython

COPY . /code
WORKDIR /code

# Install all python requires
RUN mkdir -p /deps/{build,cache,src}/ && \
    pip install --upgrade pip && \
    make develop && \
    rm -r /deps/build/ /deps/cache/
