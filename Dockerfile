FROM python:3.10-slim

WORKDIR /app

ADD python_crawler.py /app
ADD requirements.txt /app

RUN pip install --no-cache-dir -r requirements.txt

CMD ["python", "python_crawler.py"]