from flask import Flask, render_template, request
import string
import socket
from time import sleep, time
from tqdm import tqdm

app = Flask(__name__)
worker_addr = [('127.0.0.1', 12345), ('127.0.0.1', 12346), ('127.0.0.1', 12347)]
connections = [None] * len(worker_addr)  # TCP connections

PASSWORD_LEN = 5
SIZE_OF_ALPHABET = len(string.ascii_letters)
CHECK_IN_PERIOD_SEC = 3
JOB, ACK_JOB, PING, NOT_DONE, DONE_NOT_FOUND, DONE_FOUND, SHUTDOWN = range(1, 8)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/crack')
def crack():
    hash = request.args.get('md5')
    num_workers = int(request.args.get('workers'))

    start_time = time()
    create_connections(num_workers)
    distribute_task(num_workers, hash)
    password_found = False
    while not password_found:
        password_found, password = check_in(num_workers)
        if not password_found:
            print(f'sleep for {CHECK_IN_PERIOD_SEC} secs')
            sleep(CHECK_IN_PERIOD_SEC)
    end_time = time()
    print(f'Found: {password}. It took {round(end_time - start_time, 2)} seconds.')
    # TODO AJAX show password

    # stop current task among workers
    for worker_id in range(num_workers):
        send_to_client(worker_id, f'{SHUTDOWN}', listen=False)

    close_connections(num_workers)
    return render_template('crack.html', md5=hash, password=password)

def create_connections(num_workers):
    for worker_id in range(num_workers):
        soc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)    # AF_INET: IPv4, SOCK_STREAM: TCP
        soc.connect(worker_addr[worker_id])
        connections[worker_id] = soc

def close_connections(num_workers):
    for worker_id in range(num_workers):
        connections[worker_id].close()

def distribute_task(num_workers, hash):
    # TODO async send task
    # (TODO) handle not acked jobs
    # (TODO) handle failure
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
            return True, password
    return False, None

def send_to_client(worker_id, cmd, listen=True):
    '''
    return a list consisting of command and arguments
    '''
    # with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as soc:
    soc = connections[worker_id]
    # send command
    soc.send(cmd.encode())
    print(f'Sent to {worker_id}: {cmd}')

    if listen:
        # listen for response
        data = soc.recv(1024)  # receive byte streams with 1024-byte buffer
        response = data.decode()
        print(f'Recv fr {worker_id}: {response}')
        response = response.split(' ')
        response[0] = int(response[0])
        return response

def n_to_nums(n, b=SIZE_OF_ALPHABET):
    """Convert a positive number n to its digit representation in base b."""
    digits = []
    while n > 0:
        digits.append(n % b)
        n  = n // b
    # pad to PASSWORD_LEN
    while len(digits) < PASSWORD_LEN:
        digits.append(0)
    digits.reverse()
    return digits

def str2nums(s):
    nums = []
    for c in s:
        if c.islower():  # 0-25 is a-z
            nums.append(ord(c) - ord('a'))
        else:  # 26-51 is A-Z
            nums.append(ord(c) + 26 - ord('A'))
    return nums

def nums2str(nums):
    str_builder = []
    for n in nums:
        if n < 26:  # 0-25 is a-z
            str_builder.append(chr(n + ord('a')))
        else:  # 26-51 is A-Z
            str_builder.append(chr(n - 26 + ord('A')))
    return ''.join(str_builder)

# A-Z: 65-90, a-z: 97-122
def str_generator(start_s, end_s):
    # assuming start_s < end_s and are valid strings
    start_nums, end_nums = str2nums(start_s), str2nums(end_s)
    nums = start_nums
    while nums <= end_nums:
        yield nums2str(nums)

        # increment by 1
        i = len(nums) - 1
        while i >= 0:
            nums[i] = nums[i] + 1
            if nums[i] < SIZE_OF_ALPHABET:
                break
            nums[i] = 0
            i -= 1
        if i < 0:
            return

if __name__ == '__main__':
    print(nums2str(list(range(SIZE_OF_ALPHABET))))
    print(str2nums(string.ascii_letters))

    print(n_to_nums(100))
 