# Welcome to RabbitMQ message consumer
# Each message which will be received, will be forwarded to the configured mail

import pika
import logging
import smtplib
import ssl
import time

RABBITMQ_HOST = "msg-p-slink"
RABBITMQ_QUEUE = "new_link"

# MAIL CONSTANTS #
SENDER_NAME = "SLinker"
SENDER_MAIL = "yonka2017y@gmail.com"

# https://stackoverflow.com/questions/72478573/how-to-send-an-email-using-python-after-googles-policy-update-on-not-allowing-j
SENDER_MAIL_PASSWORD = "?"  # App password (need 2FA on to enable this option)


RECEIVER_NAME = "Admin"
RECEIVER_MAIL = "yonka2003@gmail.com"

PORT = 465  # SSL Connection
SMTP_SERVER = "smtp.gmail.com"


def main():
    logging.basicConfig(level=logging.INFO)
    logging.getLogger('pika').setLevel(logging.CRITICAL)  # set pika (RabitMQ) logs only on critical mode

    time.sleep(3)  # wait 3 seconds until server.py will create the RabbitMQ queue

    # Connect to the RabbitMQ server
    connection = pika.BlockingConnection(pika.ConnectionParameters(host=RABBITMQ_HOST))
    channel = connection.channel()

    # Tell RabbitMQ to call the callback function for every message
    channel.basic_consume(queue=RABBITMQ_QUEUE, on_message_callback=callback, auto_ack=True)

    logging.info(" [MSG-C] Waiting for messages..")
    channel.start_consuming()


# Define a callback function to handle incoming messages
def callback(ch, method, properties, body):
    logging.info(" [MSG-C] Got message, forwarding to mail..")
    forward_mail(body, RECEIVER_MAIL)


def forward_mail(msg, to_mail):
    # Create a secure SSL context
    context = ssl.create_default_context()

    mime_txt = f"""From: From {SENDER_NAME} <{SENDER_MAIL}>
To: To {RECEIVER_NAME} <{RECEIVER_MAIL}>
Subject: SLink - New link notification

""" + msg.decode()

    with smtplib.SMTP_SSL(SMTP_SERVER, PORT, context=context) as server:

        server.login(SENDER_MAIL, SENDER_MAIL_PASSWORD)  # login smtp server
        server.sendmail(SENDER_MAIL, to_mail, mime_txt.encode())  # send mail thru smtp server
        logging.info(f" [MSG-C] Mail have been sent to {to_mail}")


if __name__ == '__main__':
    main()
