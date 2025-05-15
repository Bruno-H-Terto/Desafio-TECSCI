from http import HTTPStatus

from sqlalchemy import select

from src.app.models import Inverter, Plant


def test_create_inverter(client, session):
    plant = Plant(plant_name='Test Plant')
    session.add(plant)
    session.commit()
    session.refresh(plant)

    response = client.post('/inverters', json={'plant_id': plant.id})

    assert response.status_code == HTTPStatus.CREATED
    assert response.json() == {'id': 1, 'plant_id': plant.id}


def test_user_sees_all_inverters(client, session):
    plant = Plant(plant_name='Test Plant')
    session.add(plant)
    session.commit()
    session.refresh(plant)

    inverter1 = Inverter(plant_id=plant.id)
    inverter2 = Inverter(plant_id=plant.id)
    session.add_all([inverter1, inverter2])
    session.commit()
    session.refresh(inverter1)
    session.refresh(inverter2)

    response = client.get('/inverters')

    assert response.status_code == HTTPStatus.OK
    assert response.json()['inverters'] == [
        {'id': 1, 'plant_id': plant.id},
        {'id': 2, 'plant_id': plant.id},
    ]


def test_list_inverters_with_params(client, session):
    number_of_inverters = 3
    plant1 = Plant(plant_name='Plant 1')
    plant2 = Plant(plant_name='Plant 2')
    session.add_all([plant1, plant2])
    session.commit()
    session.refresh(plant1)
    session.refresh(plant2)

    inverter1 = Inverter(plant_id=plant1.id)
    inverter2 = Inverter(plant_id=plant1.id)
    inverter3 = Inverter(plant_id=plant1.id)
    inverter4 = Inverter(plant_id=plant2.id)
    session.add_all([inverter1, inverter2, inverter3, inverter4])
    session.commit()

    response = client.get(f'/inverters?limit=4&offset=0&plant_id={plant1.id}')

    assert response.status_code == HTTPStatus.OK

    data = response.json()
    assert len(data['inverters']) == number_of_inverters
    assert data['inverters'][0]['plant_id'] == plant1.id
    assert data['inverters'][1]['plant_id'] == plant1.id
    assert data['inverters'][2]['plant_id'] == plant1.id


def test_show_inverter(client, session):
    plant = Plant(plant_name='Test Plant')
    session.add(plant)
    session.commit()
    session.refresh(plant)

    inverter = Inverter(plant_id=plant.id)
    session.add(inverter)
    session.commit()
    session.refresh(inverter)

    response = client.get(f'/inverters/{inverter.id}')

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {'id': inverter.id, 'plant_id': plant.id}


def test_show_inverter_not_found(client):
    response = client.get('/inverters/999')

    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json() == {'detail': 'Inverter not found'}


def test_update_inverter(client, session):
    plant1 = Plant(plant_name='Plant 1')
    plant2 = Plant(plant_name='Plant 2')
    session.add_all([plant1, plant2])
    session.commit()
    session.refresh(plant1)
    session.refresh(plant2)

    inverter = Inverter(plant_id=plant1.id)
    session.add(inverter)
    session.commit()
    session.refresh(inverter)

    response = client.put(f'/inverters/{inverter.id}', json={'plant_id': plant2.id})

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {'id': inverter.id, 'plant_id': plant2.id}

    updated_inverter = session.scalar(select(Inverter).where(Inverter.id == inverter.id))
    assert updated_inverter.plant_id == plant2.id


def test_update_non_existing_inverter(client):
    response = client.put('/inverters/999', json={'plant_id': 1})

    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json() == {'detail': 'Inverter not found'}


def test_delete_existing_inverter(client, session):
    plant = Plant(plant_name='Test Plant')
    session.add(plant)
    session.commit()
    session.refresh(plant)

    inverter = Inverter(plant_id=plant.id)
    session.add(inverter)
    session.commit()
    session.refresh(inverter)

    response = client.delete(f'/inverters/{inverter.id}')

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {'message': 'Inverter deleted'}

    deleted = session.scalar(select(Inverter).where(Inverter.id == inverter.id))
    assert deleted is None


def test_delete_non_existing_inverter(client):
    response = client.delete('/inverters/999')

    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json() == {'detail': 'Inverter not found'}
