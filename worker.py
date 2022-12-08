import socket
import argparse
import multiprocessing
import threading
from hashlib import md5
from tqdm import tqdm
from app import str_generator, SIZE_OF_ALPHABET
from time import sleep


ap = argparse.ArgumentParser()
ap.add_argument("-p", "--port", required=True, help="port number of the server")
args = vars(ap.parse_args())

JOB, ACK_JOB, PING, NOT_DONE, DONE_NOT_FOUND, DONE_FOUND, SHUTDOWN = range(1, 8)

def brute_force(start_s, end_s, hash):
    # TODO use multiprocessing
    global job_done, password, shutdown
    for s in tqdm(str_generator(start_s, end_s), total = SIZE_OF_ALPHABET ** 5):
        # hashes
        # 'ABC': '902fbdd2b1df0c4f70b4a5d23525e932'
        # 'abcde': 'ab56b4d92b40713acc5af89985d4b786'
        # 'ABCDE': '2ecdde3959051d913f61b14579ea136d'
        if md5(s.encode()).hexdigest() == hash:
            tqdm.write(f'found: {s}')
            job_done, password = True, s
            return
            # return True, s
        if shutdown:
            return
    # return False, None
    job_done, password = False, None

shutdown = False
daemon = None
job_done, password = False, None
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as soc:  # AF_INET: IPv4, SOCK_STREAM: TCP
    HOST = ''
    PORT = int(args['port'])  # port of server

    soc.bind((HOST, PORT))
    soc.listen()
    conn = None
    conn, address = soc.accept()
    print('Connected')
    while True:
        job_done, password = False, None
        while True:
            data = conn.recv(1024)  # receive byte streams with 1024-byte buffer
            if not data:  # disconnected
                print('Disconnected. Waiting for connection.')
                conn, address = soc.accept()
                print('Connected')
                break

            request = data.decode().split(' ')
            cmd = int(request[0])
            if cmd == JOB:
                _, start_s, end_s, hash = request
                conn.sendall(f'{ACK_JOB} {start_s} {end_s} {hash}'.encode())
                # job_done, password = brute_force(start_s, end_s, hash)
                shutdown = False
                daemon = threading.Thread(target=brute_force, args=(start_s, end_s, hash,), daemon=True)
                daemon.start()
            elif cmd == PING:
                print(job_done, password)
                if not job_done:
                    conn.sendall(f'{NOT_DONE}'.encode())
                else:
                    if password:
                        conn.sendall(f'{DONE_FOUND} {password} {hash}'.encode())
                    else:
                        conn.sendall(f'{DONE_NOT_FOUND} {start_s} {end_s}'.encode())
            elif cmd == SHUTDOWN:
                print('Received shutdown.')
                shutdown = True
            else:
                raise ValueError('Incorrect command value')
