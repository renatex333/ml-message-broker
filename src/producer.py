import os
import pika
import json
import random
from time import sleep
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

    # Create a queue name
    queue = os.getenv("RABBIT_QUEUE")
    channel.queue_declare(queue=queue, durable=True)

    print("Sending messages. To stop press CTRL+C...")

    try:
        while True:
            # Generate random JSON data
            data = {
                "age": random.randint(18, 65),
                "job": random.choice(
                    ["blue-collar", "entrepreneur", "housemaid", "management", "retired",
                     "self-employed", "services", "student", "technician", "unemployed", "unknown"]
                ),
                "marital": random.choice(
                    ["single", "married"]
                ),
                "education": random.choice(
                    ["unknown", "secondary", "tertiary"]
                ),
                "balance": random.randint(-400, 10000),
                "housing": random.choice(["yes", "no"]),
                "duration": random.randint(1, 500),
                "campaign": random.randint(1, 10)
            }

            # Convert data to JSON string
            msg = json.dumps(data)

            # Send a message to queue
            channel.basic_publish(
                exchange="",
                routing_key=queue,
                body=msg,
            )

            # Delay message sending
            sleep(3)

    except KeyboardInterrupt:
        connection.close()

if __name__ == "__main__":
    main()
