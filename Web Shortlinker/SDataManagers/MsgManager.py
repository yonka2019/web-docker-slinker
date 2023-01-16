import pika
import logging

RABBITMQ_HOST = "msg-slink"
RABBITMQ_QUEUE = "new_link"


class MsgManager:  # RabbitMQ management
    @staticmethod
    def create_queue():  # only one time on server run
        # Connect to the RabbitMQ server
        connection = pika.BlockingConnection(pika.ConnectionParameters(host=RABBITMQ_HOST))
        channel = connection.channel()

        channel.queue_declare(queue=RABBITMQ_QUEUE)
        logging.info(f" [MSG-P] Queue '{RABBITMQ_QUEUE} have been created'")

        connection.close()

    @staticmethod
    def publish_message(short_url, original_url):  # public message into rabbitmq queue about new short-link
        connection = pika.BlockingConnection(pika.ConnectionParameters(host=RABBITMQ_HOST))
        channel = connection.channel()

        message_to_publish = f"New link have been created!\n" \
                             f"['{short_url}' : '{original_url}']".encode()

        channel.basic_publish(exchange='', routing_key=RABBITMQ_QUEUE, body=message_to_publish)
        logging.info(" [MSG-P] New link message published successfully!")

        connection.close()
