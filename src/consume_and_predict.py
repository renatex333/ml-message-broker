import os
import pika
import json
import functools
import pandas as pd
from time import sleep
from dotenv import load_dotenv
from model import load_model, load_encoder

def main():
    load_dotenv()

    ml_models = {}
    ml_models["ohe"] = load_encoder()
    ml_models["models"] = load_model()

    # Configure credentials
    credentials = pika.PlainCredentials(
        os.getenv("RABBIT_USERNAME"), os.getenv("RABBIT_PASSWORD")
    )

    # Create a connection
    connection = pika.BlockingConnection(
        pika.ConnectionParameters("localhost", credentials=credentials, heartbeat=0)
    )

    channel = connection.channel()

    # Declare queues
    queue = os.getenv("RABBIT_QUEUE")
    prediction_queue = os.getenv("RABBIT_PREDICTION_QUEUE")
    channel.queue_declare(queue=queue, durable=True)
    channel.queue_declare(queue=prediction_queue, durable=True)

    # Configures which function should process the messages
    predict_callback = functools.partial(
        predict, ml_models=ml_models, reply_queue=prediction_queue
    )
    channel.basic_consume(
        queue=queue,
        on_message_callback=predict_callback,
        auto_ack=False,
    )

    print("Waiting for messages. To exit press CTRL+C...")

    try:
        channel.start_consuming()
    except KeyboardInterrupt:
        channel.stop_consuming()

    connection.close()

def predict(ch, method, properties, body, ml_models, reply_queue):
    """
    Define callback function (consumer function)
    """
    # Load the models
    ohe = ml_models["ohe"]
    model = ml_models["models"]
    print("Received message:", body)

    df_person = pd.DataFrame([json.loads(body)])

    person_t = ohe.transform(df_person)
    prediction = model.predict(person_t)[0]
    print(f"Prediction: {prediction}")

    df_person["prediction"] = prediction

    msg = df_person.to_json(index=False)

    # Send a message to queue
    print("Sending prediction...")
    ch.basic_publish(
        exchange="",
        routing_key=reply_queue,
        body=msg,
    )

    # Notify RabbitMQ that message was processed
    ch.basic_ack(method.delivery_tag)

if __name__ == "__main__":
    main()
