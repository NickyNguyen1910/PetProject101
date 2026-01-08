FROM python:3.10-slim

WORKDIR /app

ADD requirements.txt /app

RUN pip install --no-cache-dir -r requirements.txt

ADD python_crawler.py /app

CMD ["python", "python_crawler.py"]