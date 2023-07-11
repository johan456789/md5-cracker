import os
import string

MAX_NUM_WORKERS = 3
PASSWORD_LEN = int(os.environ.get('PASSWORD_LEN', '3'))
SIZE_OF_ALPHABET = len(string.ascii_letters)
CHECK_IN_PERIOD_SEC = 3
JOB, ACK_JOB, PING, NOT_DONE, DONE_NOT_FOUND, DONE_FOUND, SHUTDOWN = range(1, 8)
