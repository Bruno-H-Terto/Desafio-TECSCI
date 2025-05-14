from http import HTTPStatus


def test_check_root_path(client):
    response = client.get('/')

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {'Hello': 'World'}
