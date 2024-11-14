FROM python:3.12-alpine

RUN apk add ansible sshpass openssh

WORKDIR /app

RUN pip install --upgrade pip
COPY requirements.txt /app/
WORKDIR /app
RUN pip install -r requirements.txt

RUN adduser --disabled-password --gecos "" user
RUN chown -R user /app

USER user

COPY . .
