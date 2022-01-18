FROM python:3.7-slim

WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN pip install --upgrade pip

COPY . .

RUN pip3 install -r requirements.txt --no-cache-dir
##
#CMD ["gunicorn", "backend.wsgi:application", "--bind", "0.0.0.0:8000" ]