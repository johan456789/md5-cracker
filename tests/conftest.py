# fixtures
import os
import pytest
from subprocess import Popen
import time

import requests


from config import get_config
from utils import get_free_ports, set_env_vars
from utils.network import Network


@pytest.fixture(autouse=True)
def set_test_env_vars():
    config = get_config('test')
    set_env_vars(config)
    print('env vars set')


@pytest.fixture(scope="module")
def network():
    config = get_config('test')
    set_env_vars(config)
    MAX_NUM_WORKERS = int(os.environ.get('MAX_NUM_WORKERS'))  # type: ignore
    ports = get_free_ports(MAX_NUM_WORKERS)
    network = Network(ports)
    return network


@pytest.fixture(scope="module")
def server():
    # Setup - Start the server and workers
    server_process = Popen(['python', 'app.py'])

    # wait for the server to be ready
    max_retries = 10
    retry_interval = 1  # seconds
    retries = 0
    while retries < max_retries:
        try:
            response = requests.get('http://localhost:5678')  # Replace with your server's URL
            response.raise_for_status()
            break  # Server is up and running, exit the loop
        except (requests.RequestException, ConnectionError):
            retries += 1
            time.sleep(retry_interval)
    print(f'server ready after {retries} retries')

    yield  # start the test

    # Teardown - Terminate the processes
    server_process.kill()
