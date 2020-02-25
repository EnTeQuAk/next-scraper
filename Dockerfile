FROM python:3.8-slim-buster

RUN apt-get update && apt-get install -y \
    gcc \
    build-essential

ENV PIP_BUILD=/deps/build/
ENV PIP_CACHE_DIR=/deps/cache/
ENV PIP_SRC=/deps/src/

# supervisord to run services
RUN pip install supervisor
RUN pip install watchdog[watchmedo]

# Preserve bash history across image updates.
# This works best when you link your local source code
# as a volume.
ENV HISTFILE /code/docker/artifacts/bash_history

# Configure bash history.
ENV HISTSIZE 50000
ENV HISTIGNORE ls:exit:"cd .."

# This prevents dupes but only in memory for the current session.
ENV HISTCONTROL erasedups

COPY . /code
WORKDIR /code

# Install all python requires
RUN mkdir -p /deps/{build,cache,src}/ && \
    pip install --upgrade pip && \
    make develop && \
    rm -r /deps/build/ /deps/cache/
