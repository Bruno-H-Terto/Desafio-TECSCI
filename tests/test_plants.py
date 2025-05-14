from http import HTTPStatus


def test_create_plant(client):
    response = client.post('/plants', json={'plant_name': 'US-01'})

    assert response.status_code == HTTPStatus.CREATED
    assert response.json() == {'id': 1, 'plant_name': 'US-01'}


def test_the_plant_name_cannot_be_blank(client):
    response = client.post('/plants', json={'plant_name': ''})

    assert response.status_code == HTTPStatus.UNPROCESSABLE_ENTITY
    assert response.json()['detail'][0]['msg'] == 'Value error, O nome da usina não pode estar em branco'


def test_user_sees_all_plants(client, plants):
    response = client.get('/plants')

    assert response.status_code == HTTPStatus.OK
    assert response.json()['plants'] == [
        {'id': 1, 'plant_name': 'US-1'},
        {'id': 2, 'plant_name': 'US-2'},
        {'id': 3, 'plant_name': 'US-3'},
        {'id': 4, 'plant_name': 'US-4'},
        {'id': 5, 'plant_name': 'US-5'},
    ]


def test_pagination(client, plants):
    number_plants = 3
    response = client.get('/plants?limit=3&offset=1')

    assert response.status_code == HTTPStatus.OK
    data = response.json()

    assert len(data['plants']) == number_plants
