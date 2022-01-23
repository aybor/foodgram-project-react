FROM arm64v8/python:3.7-slim

WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN pip3 install --upgrade pip

COPY . .

RUN pip3 install -r requirements.txt --no-cache-dir
