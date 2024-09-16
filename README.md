# Message Broker with RabbitMQ and Celery

Welcome to this ML project! This application leverages RabbitMQ to create and manage queues for producers and subscribers, enabling data to be processed, predicted upon, and the results posted to new queues. Additionally, it uses Celery to handle distributed task queues, facilitating efficient task management across multiple workers.

## Project Structure

- **`models/`**: Contains machine learning models and encoders.
- **`src/`**: Contains the main source code for producer and subscriber scripts.

## Setup Instructions

### 1. Installing Dependencies

To install all necessary dependencies, run the following command:

```bash
pip install -r requirements.txt
```

### 2. Starting RabbitMQ with Docker

To start the RabbitMQ container, use the following commands:

```bash
docker compose build
docker compose up
```

Check if the RabbitMQ dashboard is running at [http://localhost:15672](http://localhost:15672).

### 3. Using RabbitMQ

[RabbitMQ](https://www.rabbitmq.com/tutorials) is an open-source message broker that simplifies messaging between distributed systems via the AMQP protocol. In this project, we implement a producer-consumer model where data is passed between components using queues.

#### Running Producers and Subscribers

To observe the producer and subscriber workflow, run each command in separate terminal windows:

```bash
python3 src/RabbitMQ/producer.py
python3 src/RabbitMQ/consume_and_predict.py
python3 src/RabbitMQ/consume_prediction.py
```

This will execute the producer, make predictions using a subscriber, and post the predictions on a new queue.

## Celery: Distributed Task Queue System

[Celery](https://docs.celeryq.dev/en/stable/getting-started/index.html) is a distributed task queue system written in Python, designed for managing asynchronous task execution. Celery is built on a producer-consumer model and uses a message broker, such as RabbitMQ, to communicate between task producers (clients) and task executors (workers).

### Running Celery with Docker

To start the RabbitMQ container for Celery, use the same commands as RabbitMQ:

```bash
docker compose build
docker compose up
```

Check if the RabbitMQ dashboard is running at [http://localhost:15672](http://localhost:15672).

### Running Celery Workers

Run the following commands in separate terminal windows within the `src/Celery` directory:

1. Start the Celery worker:

```bash
celery -A ml_app worker --autoscale=10,2
```

2. Start the Celery Flower monitoring tool:

```bash
celery -A ml_app flower
```

3. Start the producer:

```bash
python3 producer.py
```

The producer will prompt you to enter a message. Once you enter a message, it will send it to the Celery worker via the `predict` task.

Check the Celery Flower dashboard at [http://0.0.0.0:5555](http://0.0.0.0:5555) to monitor tasks and worker activity.

## References

- [RabbitMQ Tutorials](https://www.rabbitmq.com/tutorials)
- [Celery Documentation](https://docs.celeryq.dev/en/stable/getting-started/index.html)