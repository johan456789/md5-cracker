import socket
from typing import List, Tuple

from utils.constants import ACK_JOB, DONE_FOUND, JOB, PASSWORD_LEN, PING, SIZE_OF_ALPHABET  # noqa
from utils.str_num import n_to_nums, nums2str

PORT1, PORT2, PORT3 = range(12340, 12343)
if socket.gethostname() == 'Johans-MacBook-Air.local':
    LOCALHOST = '127.0.0.1'
    worker_addr: List[Tuple[str, int]] = [(LOCALHOST, PORT1),
                                          (LOCALHOST, PORT2),
                                          (LOCALHOST, PORT3)]
else:
    worker_addr: List[Tuple[str, int]] = [('172.17.3.33', PORT1),
                                          ('172.17.3.34', PORT2),
                                          ('172.17.3.35', PORT3)]
print(f'worker_addr: {worker_addr}')
connections = [None] * len(worker_addr)  # TCP connections


def create_connections(num_workers):
    """
    Create TCP connections to worker nodes.

    Args:
        num_workers (int): The number of workers.

    Returns:
        list[socket.socket]: A list of TCP connections to worker nodes.
    """
    for worker_id in range(num_workers):
        # AF_INET: IPv4, SOCK_STREAM: TCP
        soc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        soc.connect(worker_addr[worker_id])
        connections[worker_id] = soc  # type: ignore
        assert connections[worker_id] is not None
    return connections


def close_connections(connections):
    """
    Close all connections in the given list of connections.

    Args:
        connections (List[socket.socket]):
            A list of socket objects representing the connections to be closed.

    Returns:
        None
    """
    for conn in connections:
        if conn:
            conn.close()


def distribute_task(num_workers, hash):
    """
    Distribute the task of cracking the password to multiple workers.

    Args:
        num_workers (int): The number of workers to distribute the task to.
        hash (str): The hash of the password to crack.

    Returns:
        None
    """
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
            response = send_to_client(worker_id, f'{JOB} {start_s} {end_s} {hash}')  # noqa
            if response[0] == ACK_JOB:
                job_acked = True

        start += step
        worker_id = (worker_id + 1) % num_workers


def check_in(num_workers):
    """
    Check in with all workers and return the password
    if it's cracked else None.

    Args:
        num_workers (int): The number of workers to check in with.

    Returns:
        str: The password if it's cracked, else None.
    """
    # (TODO) handle DONE_NOT_FOUND
    for worker_id in range(num_workers):
        response = send_to_client(worker_id, f'{PING}')
        if response[0] == DONE_FOUND:
            password, _ = response[1], response[2]
            return password
    return None


def send_to_client(worker_id: int, cmd: str, listen: bool = True) -> List:
    """
    Sends a command to a worker and waits for a response.

    Args:
        worker_id (int): The ID of the worker to send the command to.
        cmd (str): The command to send to the worker. The constant is
                    defined in utils/constants.py.
        listen (bool): Whether to wait for a response from the worker.

    Returns:
        list: A list representing the response from the worker
                consisting of command and arguments. Returns an empty list if
                listen is False.

    Example:
        >>> send_to_client(1, PING, True)
        [NOT_DONE]
        >>> send_to_client(1, PING, False)
        [DONE_FOUND, 'password', 'hash']
    """
    soc = connections[worker_id]
    if soc is None:
        raise ValueError(f'No connection to worker {worker_id}')
    soc.send(cmd.encode())
    print(f'Sent to {worker_id}: {cmd}')

    response = ['']
    if listen:
        # listen for response
        data = soc.recv(1024)  # receive byte streams with 1024-byte buffer
        response = data.decode()
        print(f'Recv fr {worker_id}: {response}')
        response = response.split(' ')
        response[0] = int(response[0])  # type: ignore
    return response
