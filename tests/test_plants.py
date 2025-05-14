from http import HTTPStatus

from sqlalchemy import select

from src.api.models import Plant


def test_create_plant(client):
    response = client.post('/plants', json={'plant_name': 'US-01'})

    assert response.status_code == HTTPStatus.CREATED
    assert response.json() == {'id': 1, 'plant_name': 'US-01'}


def test_the_plant_name_cannot_be_blank(client):
    response = client.post('/plants', json={'plant_name': ''})

    assert response.status_code == HTTPStatus.UNPROCESSABLE_ENTITY
    assert response.json()['detail'][0]['msg'] == 'Value error, plant_name cannot be blank'


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


def test_show_plant(client, session):
    plant = Plant(plant_name='Test Plant')
    session.add(plant)
    session.commit()
    session.refresh(plant)

    response = client.get(f'/plants/{plant.id}')

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {'id': plant.id, 'plant_name': 'Test Plant'}


def test_show_plant_not_found(client):
    response = client.get('/plants/999')

    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json() == {'detail': 'Plant not found'}


def test_update_plant(client, session):
    plant = Plant(plant_name='Test Plant')
    session.add(plant)
    session.commit()
    session.refresh(plant)

    response = client.put(f'/plants/{plant.id}', json={'plant_name': 'US-01'})

    assert response.json() == {'id': plant.id, 'plant_name': 'US-01'}
    assert response.status_code == HTTPStatus.OK


def test_update_non_existing_plant(client):
    response = client.put('/plants/999', json={'plant_name': 'US-01'})

    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json() == {'detail': 'Plant not found'}


def test_update_plant_with_duplicate_name(client, session):
    plant1 = Plant(plant_name='BR-01')
    plant2 = Plant(plant_name='US-01')
    session.add_all([plant1, plant2])
    session.commit()
    session.refresh(plant1)
    session.refresh(plant2)

    response = client.put(f'/plants/{plant2.id}', json={'plant_name': 'BR-01'})

    assert response.status_code == HTTPStatus.FORBIDDEN
    assert response.json() == {'detail': 'plant_name already in use'}


def test_delete_existing_plant(client, session):
    plant = Plant(plant_name='BR-01')
    session.add(plant)
    session.commit()
    session.refresh(plant)

    response = client.delete(f'/plants/{plant.id}')

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {'message': 'Plant deleted'}

    deleted = session.scalar(select(Plant).where(Plant.id == plant.id))
    assert deleted is None


def test_delete_non_existing_plant(client):
    response = client.delete('/plants/999')

    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json() == {'detail': 'Plant not found'}
