FROM python:3.9-alpine3.18

COPY requirements.txt /temp/requirements.txt
COPY . /vektors/
WORKDIR /vektors/
EXPOSE 8000

RUN apk add postgresql-client build-base postgresql-dev

RUN pip install --upgrade pip -r /temp/requirements.txt
