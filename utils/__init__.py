import os
import socket


def set_env_vars(obj):
    env_vars = {attr: str(getattr(obj, attr)) for attr in dir(obj) if "__" not in attr}
    os.environ.update(env_vars)


def get_free_port():
    s = socket.socket()
    s.bind(('', 0))
    port = s.getsockname()[1]
    s.close()
    return port


def get_free_ports(num_ports):
    return [get_free_port() for _ in range(num_ports)]
