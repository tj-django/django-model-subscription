FROM python:3.8-slim-buster as builder

ENV PYTHONUNBUFFERED 1

WORKDIR /

RUN apt-get update \
  && apt-get install -y build-essential \
      # Translations dependencies
      gettext

# Clean up unused files
RUN apt-get purge -y --auto-remove -o APT::AutoRemove::RecommendsImportant=false \
  && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .

RUN pip3 install -U pip setuptools \
    && pip3 install -r requirements.txt

COPY . /app
WORKDIR /app
