from http import HTTPStatus

from sqlalchemy import select

from src.api.models import Inverter, Plant


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
    plant = Plant(plant_name='Test Plant')
    session.add(plant)
    session.commit()
    session.refresh(plant)

    inverter = Inverter(plant_id=plant.id)
    session.add(inverter)
    session.commit()
    session.refresh(inverter)

    response = client.put(f'/inverters/{inverter.id}', json={'plant_id': plant.id})

    assert response.json() == {'id': inverter.id, 'plant_id': plant.id}
    assert response.status_code == HTTPStatus.OK


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
