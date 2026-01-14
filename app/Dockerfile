FROM tiangolo/uvicorn-gunicorn-fastapi:python3.10-slim

WORKDIR /app

ADD requirements.txt /app

RUN pip install --no-cache-dir -r requirements.txt

COPY . /app