FROM python:3.12-alpine

RUN apk add ansible sshpass

WORKDIR /app

RUN pip install --upgrade pip
COPY requirements.txt /app/
WORKDIR /app
RUN pip install -r requirements.txt

COPY . .
