from http import HTTPStatus


def test_create_plant(client):
    response = client.post('/plants', json={'plant_name': 'US-01'})

    assert response.status_code == HTTPStatus.CREATED
    assert response.json() == {'id': 1, 'plant_name': 'US-01'}
