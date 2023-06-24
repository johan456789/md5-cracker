from unittest.mock import patch, MagicMock
from utils.network import create_connections, close_connections, distribute_task, check_in
from utils.constants import NOT_DONE, SIZE_OF_ALPHABET, PASSWORD_LEN, JOB, ACK_JOB, PING, DONE_FOUND, DONE_NOT_FOUND

@patch('utils.network.socket.socket')
def test_create_connections(mock_socket):
    mock_socket.return_value = MagicMock()
    create_connections(3)
    assert mock_socket.call_count == 3

@patch('utils.network.socket.socket')
def test_close_connections(mock_socket):
    mock_socket.return_value = MagicMock()
    connections = create_connections(3)
    close_connections(connections)
    for conn in connections:
        if conn is not None:
            assert conn.closed

@patch('utils.network.send_to_client')
def test_check_in(mock_send_to_client):
    mock_send_to_client.side_effect = [[DONE_FOUND, 'password', 'hash'], [None], [None]]
    password = check_in(3)
    assert password == 'password'
    mock_send_to_client.assert_called_once()

    mock_send_to_client.side_effect = [[None], [None], [None]]
    password = check_in(3)
    assert password is None

    # TODO test DONE_NOT_FOUND

