FROM python

WORKDIR /app

COPY . /app

# pika - RabbitMQ package
RUN pip install --no-cache-dir pika

# for sending/receive mail (via SSL connection)
EXPOSE 465

CMD ["python", "consumer.py"]
