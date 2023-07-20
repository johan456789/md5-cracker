import os
import pytest
from unittest.mock import AsyncMock, patch, MagicMock
from utils.constants import DONE_FOUND, DONE_NOT_FOUND, NOT_DONE, PING


# Tests that send_to_client raises a ValueError if there is no connection to the worker
@pytest.mark.asyncio
async def test_send_to_client_no_connection(network):
    with pytest.raises(ValueError):
        await network.send_to_client(0, PING)


@patch('utils.network.socket.socket')
def test_create_and_close_connections(mock_socket, network):
    MAX_NUM_WORKERS = int(os.environ.get('MAX_NUM_WORKERS'))  # type: ignore
    mock_socket.return_value = MagicMock()
    network.create_connections()
    assert mock_socket.call_count == MAX_NUM_WORKERS
    network.close_connections()
    for conn in network.connections:
        if conn is not None:
            assert conn.closed


@pytest.mark.asyncio
async def test_check_in_with_password_found(network):
    N = int(os.environ.get('MAX_NUM_WORKERS'))  # type: ignore
    mock_send = AsyncMock()
    network.send_to_client = mock_send

    mock_send.side_effect = [[DONE_FOUND, 'password', 'hash']] + [[None]] * (N - 1)
    password, _ = await network.check_in()

    assert password == 'password'
    mock_send.assert_called_once()


@pytest.mark.asyncio
async def test_check_in_with_no_password_found(network):
    N = int(os.environ.get('MAX_NUM_WORKERS'))  # type: ignore
    mock_send = AsyncMock()
    network.send_to_client = mock_send

    mock_send.side_effect = [[NOT_DONE]] * N
    password, finished = await network.check_in()

    assert password is None
    assert finished == 0


@pytest.mark.asyncio
async def test_check_in_with_partial_passwords_found(network):
    N = int(os.environ.get('MAX_NUM_WORKERS'))  # type: ignore
    mock_send = AsyncMock()
    network.send_to_client = mock_send

    mock_send.side_effect = [[DONE_NOT_FOUND, 'a', 'c']] + [[NOT_DONE]] * (N - 1)
    password, finished = await network.check_in()

    assert password is None
    assert finished == 3


@pytest.mark.asyncio
async def test_check_in_with_multiple_partial_passwords_found(network):
    N = int(os.environ.get('MAX_NUM_WORKERS'))  # type: ignore
    mock_send = AsyncMock()
    network.send_to_client = mock_send

    mock_send.side_effect = [[DONE_NOT_FOUND, 'a', 'c'], [DONE_NOT_FOUND, 'A', 'C']] + [[NOT_DONE]] * (N - 2)
    password, finished = await network.check_in()

    assert password is None
    assert finished == 6
