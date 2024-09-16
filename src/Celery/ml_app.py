from celery import Celery
import time

app = Celery("ml_app")

# Load the Celery configuration from celeryconfig.py
app.config_from_object("celeryconfig")


@app.task
def predict(payload):
    """Simulate a Slow Prediction function"""

    print("Received:")
    print(payload)

    # Simulate long task
    time.sleep(10)

    print("Ended processing:")
    print(payload)

    return