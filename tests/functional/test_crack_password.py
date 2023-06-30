import subprocess
import time
import requests


def test_crack_passwords():
    # Start the server and workers
    PORT1, PORT2, PORT3 = range(12340, 12343)
    server_process = subprocess.Popen(['flask', 'run', '--host=0.0.0.0', '--port=5678'])
    worker_process1 = subprocess.Popen(['python', 'worker.py', '-p', str(PORT1)])
    worker_process2 = subprocess.Popen(['python', 'worker.py', '-p', str(PORT2)])
    worker_process3 = subprocess.Popen(['python', 'worker.py', '-p', str(PORT3)])
    time.sleep(1)

    try:
        # Send a request to crack the hash
        start_time = time.time()
        response = requests.get('http://localhost:5678/crack',
                                params={'workers': 3, 'md5': '902fbdd2b1df0c4f70b4a5d23525e932'})
        end_time = time.time()

        # Check the response
        print(type(response))
        print(response)
        assert response.status_code == 200
        res_obj = response.json()
        assert res_obj['password'] == 'ABC'
        assert res_obj['duration'] is not None

        # Check the response time
        assert end_time - start_time < 4
    finally:
        # Terminate the processes
        server_process.kill()
        worker_process1.kill()
        worker_process2.kill()
        worker_process3.kill()
