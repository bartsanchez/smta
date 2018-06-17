FROM debian:stable

RUN apt-get update && apt-get install -y python-pip python3

RUN pip install -U pip
RUN pip install pipenv

RUN mkdir /app
COPY . /app

WORKDIR /app

ENV PBR_VERSION=0.0.1

RUN ["pipenv", "install", "--dev"]

CMD ./entrypoint.sh
