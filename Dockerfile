FROM python:3.8-alpine

ENV PYTHONUNBUFFERED=1

RUN apk update && apk add libffi-dev zlib-dev jpeg-dev postgresql-dev gcc python3-dev musl-dev

WORKDIR /django3

COPY requirements.txt requirements.txt

# Update package lists and install Bash
RUN apk update && apk add bash

# Set the default shell to Bash
SHELL ["/bin/bash", "-c"]

RUN pip3 install -r requirements.txt
