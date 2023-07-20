from unittest.mock import patch

from app import create_app
from config import get_config


def test_index_page_rendered_successfully(network):
    app = create_app(get_config('dev'), network)
    with app.test_client() as client:
        response = client.get('/')
        assert response.status_code == 200


def test_crack_page_rendered_successfully(network):
    app = create_app(get_config('dev'), network)
    with app.test_client() as client:
        with patch.object(network, 'check_in') as mock_check_in:
            # Configure the mock behavior
            mock_check_in.side_effect = [
                (None, 10),  # First call returns (None, 10)
                ('password123', 0)  # Second call returns ('password123', 0)
            ]

            response = client.get('/crack')
            assert response.status_code == 200


def test_progress_page_rendered_successfully(network):
    app = create_app(get_config('dev'), network)
    with app.test_client() as client:
        response = client.get('/progress')
        assert response.status_code == 200

