FROM python:3.10-slim-buster

ENV PYTHONUNBUFFERED 1

WORKDIR /app
COPY . .

EXPOSE 8000

RUN pip3 install -r requirements.txt