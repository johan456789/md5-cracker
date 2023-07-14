import os
import asyncio
import socket
from typing import List

from utils.constants import SIZE_OF_ALPHABET, JOB, ACK_JOB, PING, NOT_DONE, DONE_NOT_FOUND, DONE_FOUND
from utils.str_num import n_to_nums, nums2str, str_count


class Network:
    def __init__(self, ports):
        MAX_NUM_WORKERS = int(os.environ.get('MAX_NUM_WORKERS'))  # type: ignore
        self.idling = [True] * MAX_NUM_WORKERS  # whether a worker is idling
        self.ports = ports
        self.connections = [None] * MAX_NUM_WORKERS  # TCP connections

    def create_connections(self):
        MAX_NUM_WORKERS = int(os.environ.get('MAX_NUM_WORKERS'))  # type: ignore

        print(f'creating {MAX_NUM_WORKERS} connections')
        for worker_id in range(MAX_NUM_WORKERS):
            # AF_INET: IPv4, SOCK_STREAM: TCP
            soc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            try:
                soc.connect(('localhost', self.ports[worker_id]))
                self.connections[worker_id] = soc  # type: ignore
                assert self.connections[worker_id] is not None
            except ConnectionRefusedError as e:
                raise Exception(f'{e}: failed to connect to {self.ports[worker_id]}')
            except OSError as e:
                raise Exception(f'{e}: failed to connect to {self.ports[worker_id]}')
        print(f'connections created at {self.ports}')
        return self.connections

    def close_connections(self):
        for conn in self.connections:
            if conn:
                conn.close()

    async def distribute_task(self, hash):
        # (TODO) handle not acked jobs
        # (TODO) handle failure
        PASSWORD_LEN = int(os.environ.get('PASSWORD_LEN'))  # type: ignore
        MAX_NUM_WORKERS = int(os.environ.get('MAX_NUM_WORKERS'))  # type: ignore
        total_work = SIZE_OF_ALPHABET ** PASSWORD_LEN
        step = total_work // MAX_NUM_WORKERS // 10

        start = 0
        while start < total_work:
            await asyncio.sleep(0.1)
            for worker_id in range(MAX_NUM_WORKERS):
                if start >= total_work:
                    break
                if not self.idling[worker_id]:
                    print(f'worker {worker_id} is working, skipped')
                    continue
                start_s = nums2str(n_to_nums(start))
                end_s = nums2str(n_to_nums(min(total_work - 1, start + step - 1)))

                response = await self.send_to_client(worker_id, f'{JOB} {start_s} {end_s} {hash}')
                job_acked = response[0]
                while not job_acked:
                    # TODO set a max number of retries
                    response = await self.send_to_client(worker_id, f'{JOB} {start_s} {end_s} {hash}')  # noqa
                    if response[0] == ACK_JOB:
                        job_acked = True
                self.idling[worker_id] = False
                start += step

    async def check_in(self):
        MAX_NUM_WORKERS = int(os.environ.get('MAX_NUM_WORKERS'))  # type: ignore
        strings_checked = 0
        for worker_id in range(MAX_NUM_WORKERS):
            response = await self.send_to_client(worker_id, f'{PING}')
            status = response[0]
            print(f'worker {worker_id} report status: {status}')
            if status in (DONE_FOUND, DONE_NOT_FOUND):
                self.idling[worker_id] = True
                if status == DONE_FOUND:
                    password, _ = response[1], response[2]
                    return password, _
                elif status == DONE_NOT_FOUND:
                    _, start_s, end_s = response
                    assert start_s is not None and end_s is not None
                    strings_checked += str_count(start_s, end_s)
                    print(f'strings checked ({start_s}, {end_s}): {strings_checked}')
            elif status == NOT_DONE:
                pass
        return None, strings_checked

    async def send_to_client(self, worker_id: int, cmd: str, listen: bool = True) -> List:
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
        soc = self.connections[worker_id]
        if soc is None:
            raise ValueError(f'No connection to worker {worker_id}')
        soc.send(cmd.encode())
        print(f'Sent to worker {worker_id}: {cmd}')

        response = ['']
        if listen:
            # listen for response
            data = soc.recv(1024)  # receive byte streams with 1024-byte buffer # type: ignore
            response = data.decode()
            print(f'Recv fr worker {worker_id}: {response}')
            response = response.split(' ')
            response[0] = int(response[0])  # type: ignore
        return response
