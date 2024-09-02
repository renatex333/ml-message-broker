import os
import pika
from time import sleep
from dotenv import load_dotenv


def callback(ch, method, properties, body):
    """
    Define callback function (consumer function)
    """
    print(f"Processing: {body}")
    sleep(10)
    print(f"Done: {body}")
    # Notify RabbitMQ that message was processed
    ch.basic_ack(method.delivery_tag)

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

    # Declare a queue named "chitchat"
    channel.queue_declare(queue="chitchat", durable=True)

    # Configures which function should process the messages
    channel.basic_consume(
        queue="chitchat",
        auto_ack=False,
        on_message_callback=callback,
    )

    print("Waiting for messages. To exit press CTRL+C...")

    try:
        channel.start_consuming()
    except KeyboardInterrupt:
        channel.stop_consuming()

    connection.close()

if __name__ == "__main__":
    main()
