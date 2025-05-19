FROM python:3.10-slim-buster
LABEL maintainer="Caspian-Furniture"

ENV PYTHONNUNBUFFER=1

WORKDIR /usr/src/app

COPY ./requirements.txt .

RUN pip3 install --upgrade pip && pip install -r requirements.txt

COPY ./core .