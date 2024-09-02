# message-broker

Welcome to this ML project! It uses RabbitMQ to create and manage queues so producers and subscribers can read data, predict on it, and post predictions on a new queue.

## Start up

### Installing Dependencies

To install the project dependencies, use the `requirements.txt` file:

```sh
pip install -r requirements.txt
```

### Running docker container

To start RabbitMQ's container, simply use:

```bash
docker compose build
docker compose up
```

And checkout if the dashboard is up at http://localhost:15672

## Usage

To see producers and subscribers in action, simply run each command on a different terminal:

```bash
python3 src/producer.py
python3 src/consume_and_predict.py
python3 src/consume_prediction.py
```

## Project Structure

- `data`: Contains the data used by the model.
- `models`: Contains the machine learning models and encoders.
- `notebooks`: Contains the notebooks used for data exploration and visualization.
- `src`: Contains the main source code to producer and subscriber scripts.

# References

[RabbitMQ Tutorials](https://www.rabbitmq.com/tutorials)