import socket
import argparse
import multiprocessing

ap = argparse.ArgumentParser()
ap.add_argument("-p", "--port", required=True, help="port number of the server")
args = vars(ap.parse_args())

JOB, ACK_JOB, PING, NOT_DONE, DONE_NOT_FOUND, DONE_FOUND, SHUTDOWN = range(1, 8)

def crack(hash):
    raise NotImplementedError

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as soc:  # AF_INET: IPv4, SOCK_STREAM: TCP
    HOST = ''
    PORT = int(args['port'])  # port of server

    soc.bind((HOST, PORT))
    soc.listen()

    while True:
        server, address = soc.accept()

        while True:
            data = server.recv(1024)  # receive byte streams with 1024-byte buffer
            if not data:  # client disconnects
                break
            request = data.decode().split(' ')
            cmd = int(request[0])
            if cmd == JOB:
                _, start_s, end_s, hash = request
                server.sendall(f'{ACK_JOB} {start_s} {end_s} {hash}'.encode())
                crack(hash)
            elif cmd == PING:
                raise NotImplementedError
            elif cmd == SHUTDOWN:
                raise NotImplementedError
            else:
                raise ValueError('Incorrect command value')
