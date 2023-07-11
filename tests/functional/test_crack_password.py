import pytest
import subprocess
import time
import requests


@pytest.fixture(scope="module", params=[('abc', '900150983cd24fb0d6963f7d28e17f72'),
                                        ('bMf', 'b6efca0817e70224f8d0ae8f36a0ace9'),
                                        ('fks', '9181ab10cc2003eaa38dd19a0603ab2d'),
                                        ('ABC', '902fbdd2b1df0c4f70b4a5d23525e932')])
def password_and_hash(request):
    return request.param


@pytest.fixture(scope="module")
def server_and_workers():
    # Setup - Start the server and workers
    PORT1, PORT2, PORT3 = range(12340, 12343)
    server_process = subprocess.Popen(['flask', 'run', '--host=0.0.0.0', '--port=5678'])
    worker_process1 = subprocess.Popen(['python', 'worker.py', '-p', str(PORT1)])
    worker_process2 = subprocess.Popen(['python', 'worker.py', '-p', str(PORT2)])
    worker_process3 = subprocess.Popen(['python', 'worker.py', '-p', str(PORT3)])
    time.sleep(1)

    yield

    # Teardown - Terminate the processes
    server_process.kill()
    worker_process1.kill()
    worker_process2.kill()
    worker_process3.kill()


def test_crack_password(server_and_workers, password_and_hash):
    password, hash = password_and_hash
    response = requests.get('http://localhost:5678/crack', params={'workers': 3, 'md5': hash})

    assert response.status_code == 200
    res_obj = response.json()
    assert res_obj['password'] == password
    assert res_obj['duration'] is not None
