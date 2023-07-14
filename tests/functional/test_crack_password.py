import pytest
import requests


@pytest.fixture(scope="module", params=[('abc', '900150983cd24fb0d6963f7d28e17f72'),
                                        ])
def password_and_hash(request):
    return request.param


def test_crack_password(server, password_and_hash):
    password, hash = password_and_hash
    response = requests.get('http://localhost:5678/crack', params={'workers': 3, 'md5': hash})

    assert response.status_code == 200
    res_obj = response.json()
    assert res_obj['password'] == password
    assert res_obj['duration'] is not None
