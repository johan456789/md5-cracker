import pytest
import subprocess
import time
import requests

from utils.constants import MAX_NUM_WORKERS
from utils.network import ports


@pytest.fixture(scope="module", params=[('abc', '900150983cd24fb0d6963f7d28e17f72'),
                                        ('bMf', 'b6efca0817e70224f8d0ae8f36a0ace9'),
                                        ('fks', '9181ab10cc2003eaa38dd19a0603ab2d'),
                                        ('ABC', '902fbdd2b1df0c4f70b4a5d23525e932')])
def password_and_hash(request):
    return request.param


@pytest.fixture(scope="module")
def server_and_workers():
    # Setup - Start the server and workers
    worker_processes = []
    print(f'testing on ports: {ports}')
    for i in range(len(ports)):
        process = subprocess.Popen(['python', 'worker.py', '-p', str(ports[i])])
        worker_processes.append(process)
    server_process = subprocess.Popen(['flask', 'run', '--host=0.0.0.0', '--port=5678'])
    time.sleep(1)

    yield

    # Teardown - Terminate the processes
    server_process.kill()
    for process in worker_processes:
        process.kill()


def test_crack_password(server_and_workers, password_and_hash):
    password, hash = password_and_hash
    response = requests.get('http://localhost:5678/crack', params={'workers': 3, 'md5': hash})

    assert response.status_code == 200
    res_obj = response.json()
    assert res_obj['password'] == password
    assert res_obj['duration'] is not None
