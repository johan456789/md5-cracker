import socket
from unittest.mock import Mock
import pytest
from utils.constants import DONE_FOUND, DONE_NOT_FOUND, NOT_DONE
from worker import Job, accept_new_job, check_work_done


# Tests that set() method sets job attributes correctly
def test_set_method_with_valid_input():
    job = Job()
    job.set(1, 2, 'hash')
    assert job.is_running
    assert job.start_s == 1
    assert job.end_s == 2
    assert job.hash == 'hash'
    assert not job.is_done
    assert job.password is None


# Tests that update() method sets is_done to True and password to None when is_done is True and password is not None
def test_update_method_with_is_done_true_and_password():
    job = Job()
    job.set(1, 2, 'hash')
    job.update(True, 'password')
    assert not job.is_running
    assert job.password == 'password'


# Tests that update() method sets is_done to True and password to None when is_done is True and password is None
def test_update_method_with_is_done_true_and_password_none():
    job = Job()
    job.set(1, 2, 'hash')
    job.update(True, None)
    assert job.is_done
    assert job.password is None


# Tests that update() method sets is_done to True and password to None when is_done is False and password is None
def test_update_method_with_is_done_false_and_password_none():
    job = Job()
    job.set(1, 2, 'hash')
    job.update(False, None)
    assert not job.is_done
    assert job.password is None


# Tests that set() method raises AssertionError when is_running is True
def test_set_method_with_is_running_true():
    job = Job()
    job.set(1, 2, 'hash')
    with pytest.raises(AssertionError):
        job.set(3, 4, 'new_hash')


# Tests that accept_new_job function accepts a new job and starts a new thread to execute the brute force algorithm
def test_accept_new_job_happy_path():
    job = Job()
    conn, _ = socket.socketpair()
    start_s = 'a'
    end_s = 'b'
    hash = 'hash'
    accept_new_job(job, conn, 12345, start_s, end_s, hash)
    assert job.is_running


# Tests that the function sends the correct response code and message when the job is done and the password is found
def test_job_done_password_found():
    job = Job()
    job.is_done = True
    job.password = 'password'
    job.hash = 'hash'
    conn = Mock()
    assert check_work_done(job, conn)
    conn.sendall.assert_called_once_with(f'{DONE_FOUND} password hash'.encode())


# Tests that the function sends the correct response code and message when the job is done and the password is not found
def test_job_done_password_not_found():
    job = Job()
    job.is_done = True
    job.password = None
    job.start_s = 'start'
    job.end_s = 'end'
    conn = Mock()
    assert check_work_done(job, conn)
    conn.sendall.assert_called_once_with(f'{DONE_NOT_FOUND} start end'.encode())


# Tests that the function sends the correct response code and message when the job is not done
def test_job_not_done():
    job = Job()
    job.is_done = False
    conn = Mock()
    assert not check_work_done(job, conn)
    conn.sendall.assert_called_once_with(f'{NOT_DONE}'.encode())
