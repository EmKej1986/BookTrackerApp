FROM python:latest

ENV FLASK_APP=web

WORKDIR /web

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY . .
