import socket

from utils.constants import ACK_JOB, DONE_FOUND, JOB, PASSWORD_LEN, PING, SIZE_OF_ALPHABET
from utils.str_num import n_to_nums, nums2str

PORT1, PORT2, PORT3 = range(12340, 12343)
if socket.gethostname() == 'Johans-MacBook-Air.local':
    LOCALHOST = '127.0.0.1'
    worker_addr = [(LOCALHOST, PORT1), (LOCALHOST, PORT2), (LOCALHOST, PORT3)]
else:
    worker_addr = [('172.17.3.33', PORT1), ('172.17.3.34', PORT2), ('172.17.3.35', PORT3)]
print(f'worker_addr: {worker_addr}')
connections = [None] * len(worker_addr)  # TCP connections

def create_connections(num_workers):
    for worker_id in range(num_workers):
        soc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)    # AF_INET: IPv4, SOCK_STREAM: TCP
        soc.connect(worker_addr[worker_id])
        connections[worker_id] = soc # type: ignore

def close_connections(num_workers):
    for worker_id in range(num_workers):
        connections[worker_id].close() # type: ignore

def distribute_task(num_workers, hash):
    # TODO async send task
    # (TODO) handle not acked jobs
    # (TODO) handle failure
    # (TODO) allow different task sizes
    total_work = SIZE_OF_ALPHABET ** PASSWORD_LEN
    step = total_work // num_workers

    worker_id = 0
    start = 0
    while start < total_work:
        start_s = nums2str(n_to_nums(start))
        end_s = nums2str(n_to_nums(min(total_work - 1, start + step - 1)))

        response = send_to_client(worker_id, f'{JOB} {start_s} {end_s} {hash}')
        job_acked = response[0]
        while not job_acked:
            response = send_to_client(worker_id, f'{JOB} {start_s} {end_s} {hash}')
            if response[0] == ACK_JOB:
                job_acked = True

        start += step
        worker_id = (worker_id + 1) % num_workers

def check_in(num_workers):
    '''check in with each worker, return (True, password) if password cracked, else (False, None)'''
    # (TODO) handle DONE_NOT_FOUND
    for worker_id in range(num_workers):
        response = send_to_client(worker_id, f'{PING}')
        if response[0] == DONE_FOUND:
            password, hash = response[1], response[2]
            return password
    return None

def send_to_client(worker_id, cmd, listen=True):
    '''
    return a list consisting of command and arguments
    '''
    # with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as soc:
    soc = connections[worker_id]
    # send command
    soc.send(cmd.encode())
    print(f'Sent to {worker_id}: {cmd}')

    response = []
    if listen:
        # listen for response
        data = soc.recv(1024)  # receive byte streams with 1024-byte buffer
        response = data.decode()
        print(f'Recv fr {worker_id}: {response}')
        response = response.split(' ')
        response[0] = int(response[0])
    return response
