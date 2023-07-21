import socket
import argparse
import threading
from hashlib import md5
from tqdm import tqdm

from utils.constants import SIZE_OF_ALPHABET, JOB, ACK_JOB, PING, NOT_DONE, DONE_NOT_FOUND, DONE_FOUND, SHUTDOWN
from utils.str_num import str_generator

ap = argparse.ArgumentParser()
ap.add_argument("-p", "--port", required=True, help="port number of the server")
args = vars(ap.parse_args())
shutdown = False


class Job:
    def __init__(self):
        self.is_running = False
        self.start_s = None
        self.end_s = None
        self.hash = None
        self.is_done = False
        self.password = None

    def set(self, start_s, end_s, hash):
        assert not self.is_running
        self.is_running = True
        self.start_s = start_s
        self.end_s = end_s
        self.hash = hash
        self.is_done = False
        self.password = None

    def update(self, is_done, password):
        if is_done:
            self.is_running = False
        self.is_done = is_done
        self.password = password


def brute_force(job):
    # TODO use multiprocessing
    global shutdown
    for s in tqdm(str_generator(job.start_s, job.end_s), total=SIZE_OF_ALPHABET ** 5):
        # hashes
        # 'abcde': 'ab56b4d92b40713acc5af89985d4b786'
        # 'ABCDE': '2ecdde3959051d913f61b14579ea136d'
        if md5(s.encode()).hexdigest() == job.hash:
            tqdm.write(f'Worker at {args["port"]} found: {s}')
            job.update(True, s)
            return
        if shutdown:
            return
    job.update(True, None)


def accept_new_job(job, conn, start_s, end_s, hash):
    if job.is_running:
        raise Exception('WARNING: Received job while already working on a job.')
    job.set(start_s, end_s, hash)
    conn.sendall(f'{ACK_JOB} {job.start_s} {job.end_s} {job.hash}'.encode())
    daemon = threading.Thread(target=brute_force, args=(job,), daemon=True)
    daemon.start()


def check_work_done(job, conn) -> bool:
    print(job.is_done, job.password)
    if not job.is_done:
        conn.sendall(f'{NOT_DONE}'.encode())
        return False

    if job.password:
        conn.sendall(f'{DONE_FOUND} {job.password} {job.hash}'.encode())
    else:
        conn.sendall(f'{DONE_NOT_FOUND} {job.start_s} {job.end_s}'.encode())
    return True


def main():
    global shutdown
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as soc:  # AF_INET: IPv4, SOCK_STREAM: TCP
        HOST = ''
        PORT = int(args['port'])  # port of server

        soc.bind((HOST, PORT))
        soc.listen()
        conn, address = soc.accept()
        print('Connected')
        while not shutdown:
            job = Job()
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
                    accept_new_job(job, conn, *request[1:])
                elif cmd == PING:
                    if check_work_done(job, conn):
                        break  # get ready for next job
                elif cmd == SHUTDOWN:
                    print('Received shutdown.')
                    shutdown = True
                    break
                else:
                    print(f'Unknown command: {cmd}')
                    raise ValueError('Incorrect command value')


if __name__ == '__main__':
    main()
