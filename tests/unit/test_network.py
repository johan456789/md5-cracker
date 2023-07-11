import pytest
from unittest.mock import patch, MagicMock
from utils.network import create_connections, close_connections, check_in
from utils.constants import DONE_FOUND, DONE_NOT_FOUND, NOT_DONE


@patch('utils.network.socket.socket')
def test_create_connections(mock_socket):
    mock_socket.return_value = MagicMock()
    create_connections(3)
    assert mock_socket.call_count == 3


@patch('utils.network.socket.socket')
def test_close_connections(mock_socket):
    mock_socket.return_value = MagicMock()
    connections = create_connections(3)
    close_connections()
    for conn in connections:
        if conn is not None:
            assert conn.closed


@patch('utils.network.send_to_client')
@pytest.mark.asyncio
async def test_check_in(mock_send_to_client):
    responses = [[DONE_FOUND, 'password', 'hash'], [None], [None]]
    mock_send_to_client.side_effect = responses
    password, _ = await check_in(3)
    assert password == 'password'
    mock_send_to_client.assert_called_once()

    mock_send_to_client.side_effect = [[NOT_DONE], [NOT_DONE], [NOT_DONE]]
    password, finished = await check_in(3)
    assert password is None
    assert finished == 0

    mock_send_to_client.side_effect = [[DONE_NOT_FOUND, 'a', 'c']]
    password, finished = await check_in(1)
    assert password is None
    assert finished == 3

    mock_send_to_client.side_effect = [[DONE_NOT_FOUND, 'a', 'c'], [NOT_DONE]]
    password, finished = await check_in(2)
    assert password is None
    assert finished == 3

    mock_send_to_client.side_effect = [[DONE_NOT_FOUND, 'a', 'c'], [DONE_NOT_FOUND, 'A', 'C'], [NOT_DONE]]
    password, finished = await check_in(3)
    assert password is None
    assert finished == 6
