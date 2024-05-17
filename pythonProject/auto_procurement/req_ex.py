import requests
from celery import Celery
import yaml

app = Celery(
    'tasks',
    broker='redis://localhost:6379/0',
    broker_connection_retry_on_startup=True,
)


@app.task
def load_yaml_file(file_path):
    with open(file_path, 'r') as file:
        data = yaml.safe_load(file)
    return data


resp = requests.post(
    'http://127.0.0.1:8000/api/load_goods/',
    files={
        'file': load_yaml_file('shop1.yaml'),
    }
)