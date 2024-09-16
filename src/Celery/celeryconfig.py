import os
from dotenv import load_dotenv

load_dotenv()
rabbitmq_user = os.getenv("RABBIT_USERNAME")
rabbitmq_password = os.getenv("RABBIT_PASSWORD")

broker_url = f"amqp://{rabbitmq_user}:{rabbitmq_password}@localhost:5672//"
task_serializer = "json"
accept_content = ["json"]
timezone = "UTC"
enable_utc = True