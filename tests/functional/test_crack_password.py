import pytest
import requests


@pytest.fixture(scope="module", params=[('ABC', '902fbdd2b1df0c4f70b4a5d23525e932')])
# @pytest.fixture(scope="module", params=[('ZZZ', '0745064918b49693cca64d6b6a13d28a')])
def one_password_and_hash(request):
    return request.param


@pytest.fixture(scope="module", params=[('abc', '900150983cd24fb0d6963f7d28e17f72'),
                                        ('bMf', 'b6efca0817e70224f8d0ae8f36a0ace9'),
                                        ('fks', '9181ab10cc2003eaa38dd19a0603ab2d'),
                                        ('ABC', '902fbdd2b1df0c4f70b4a5d23525e932')])
def password_and_hash(request):
    return request.param


def test_crack_one_password(server, one_password_and_hash):
    password, hash = one_password_and_hash
    response = requests.get('http://localhost:5678/crack', params={'workers': 3, 'md5': hash})

    assert response.status_code == 200
    res_obj = response.json()
    assert res_obj['password'] == password
    assert res_obj['duration'] is not None


def test_crack_password(server, password_and_hash):
    password, hash = password_and_hash
    response = requests.get('http://localhost:5678/crack', params={'workers': 3, 'md5': hash})

    assert response.status_code == 200
    res_obj = response.json()
    assert res_obj['password'] == password
    assert res_obj['duration'] is not None
