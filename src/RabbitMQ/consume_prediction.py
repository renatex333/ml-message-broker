import os
import pika
import json
import pandas as pd
from dotenv import load_dotenv

def main():
    load_dotenv()

    # Configure credentials
    credentials = pika.PlainCredentials(
        os.getenv("RABBIT_USERNAME"), os.getenv("RABBIT_PASSWORD")
    )

    # Create a connection
    connection = pika.BlockingConnection(
        pika.ConnectionParameters("localhost", credentials=credentials, heartbeat=0)
    )

    channel = connection.channel()

    # Declare queue
    prediction_queue = os.getenv("RABBIT_PREDICTION_QUEUE")
    channel.queue_declare(queue=prediction_queue, durable=True)

    channel.basic_consume(
        queue=prediction_queue,
        on_message_callback=callback,
        auto_ack=False,
    )

    print("Waiting for messages. To exit press CTRL+C...")

    try:
        channel.start_consuming()
    except KeyboardInterrupt:
        channel.stop_consuming()

    connection.close()

def callback(ch, method, properties, body):
    """
    Define callback function (consumer function)
    """
    print("Received prediction:", body)

    # Notify RabbitMQ that message was processed
    ch.basic_ack(method.delivery_tag)

if __name__ == "__main__":
    main()
