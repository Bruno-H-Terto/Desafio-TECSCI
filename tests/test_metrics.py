from datetime import datetime, timedelta
from http import HTTPStatus

from src.api.models import Inverter, Metric


def test_get_max_power_per_day(client, session):
    inverter = Inverter(plant_id=1)
    session.add(inverter)
    session.commit()
    session.refresh(inverter)

    base_date = datetime.now()
    metrics = [
        Metric(datetime=base_date, inverter_id=inverter.id, power=100.0, temp_celsius=25),
        Metric(datetime=base_date + timedelta(hours=1), inverter_id=inverter.id, power=150.0, temp_celsius=26),
        Metric(datetime=base_date + timedelta(days=1), inverter_id=inverter.id, power=200.0, temp_celsius=27),
        Metric(datetime=base_date + timedelta(days=2), inverter_id=inverter.id, power=180.0, temp_celsius=28),
        Metric(datetime=base_date + timedelta(days=2, hours=1), inverter_id=inverter.id, power=220.0, temp_celsius=28),
    ]
    session.add_all(metrics)
    session.commit()

    start_date = base_date.date()
    end_date = base_date.date() + timedelta(days=1)

    response = client.get(f'/metrics/max_power/{inverter.id}', params={'start_date': start_date, 'end_date': end_date})

    assert response.status_code == HTTPStatus.OK
    data = response.json()

    assert data == {
        'inverter_id': inverter.id,
        'metrics': [
            {'date': (base_date.date()).isoformat(), 'power': 150.0},
            {'date': (base_date.date() + timedelta(days=1)).isoformat(), 'power': 200.0},
        ],
    }


def test_get_max_power_per_day_invalid_dates(client, session):
    inverter = Inverter(plant_id=1)
    session.add(inverter)
    session.commit()
    session.refresh(inverter)

    base_date = datetime.now()
    metrics = [
        Metric(datetime=base_date, inverter_id=inverter.id, power=100.0, temp_celsius=25),
        Metric(datetime=base_date + timedelta(hours=1), inverter_id=inverter.id, power=150.0, temp_celsius=26),
        Metric(datetime=base_date + timedelta(days=1), inverter_id=inverter.id, power=200.0, temp_celsius=27),
        Metric(datetime=base_date + timedelta(days=2), inverter_id=inverter.id, power=180.0, temp_celsius=28),
        Metric(datetime=base_date + timedelta(days=2, hours=1), inverter_id=inverter.id, power=220.0, temp_celsius=28),
    ]
    session.add_all(metrics)
    session.commit()

    start_date = base_date.date()
    end_date = base_date.date() - timedelta(days=1)

    response = client.get(f'/metrics/max_power/{inverter.id}', params={'start_date': start_date, 'end_date': end_date})

    assert response.status_code == HTTPStatus.UNPROCESSABLE_ENTITY
    assert response.json() == {'detail': 'Start date cannot be less than the end date'}


def test_get_avarege_temp_celsius_per_day(client, session):
    inverter = Inverter(plant_id=1)
    session.add(inverter)
    session.commit()
    session.refresh(inverter)

    base_date = datetime.now()
    metrics = [
        Metric(datetime=base_date, inverter_id=inverter.id, power=100.0, temp_celsius=25),
        Metric(datetime=base_date + timedelta(hours=1), inverter_id=inverter.id, power=150.0, temp_celsius=26),
        Metric(datetime=base_date + timedelta(days=1), inverter_id=inverter.id, power=200.0, temp_celsius=27),
        Metric(datetime=base_date + timedelta(days=2), inverter_id=inverter.id, power=180.0, temp_celsius=28),
        Metric(datetime=base_date + timedelta(days=2, hours=1), inverter_id=inverter.id, power=220.0, temp_celsius=28),
    ]
    session.add_all(metrics)
    session.commit()

    start_date = base_date.date()
    end_date = base_date.date() + timedelta(days=1)

    response = client.get(
        f'/metrics/average_temp/{inverter.id}', params={'start_date': start_date, 'end_date': end_date}
    )

    assert response.status_code == HTTPStatus.OK
    data = response.json()

    assert data == {
        'inverter_id': inverter.id,
        'metrics': [
            {'date': (base_date.date()).isoformat(), 'temp_celsius': 25.5},
            {'date': (base_date.date() + timedelta(days=1)).isoformat(), 'temp_celsius': 27.0},
        ],
    }


def test_get_avarege_temp_celsius_per_day_invalid_dates(client, session):
    inverter = Inverter(plant_id=1)
    session.add(inverter)
    session.commit()
    session.refresh(inverter)

    base_date = datetime.now()
    metrics = [
        Metric(datetime=base_date, inverter_id=inverter.id, power=100.0, temp_celsius=25),
        Metric(datetime=base_date + timedelta(hours=1), inverter_id=inverter.id, power=150.0, temp_celsius=26),
        Metric(datetime=base_date + timedelta(days=1), inverter_id=inverter.id, power=200.0, temp_celsius=27),
        Metric(datetime=base_date + timedelta(days=2), inverter_id=inverter.id, power=180.0, temp_celsius=28),
        Metric(datetime=base_date + timedelta(days=2, hours=1), inverter_id=inverter.id, power=220.0, temp_celsius=28),
    ]
    session.add_all(metrics)
    session.commit()

    start_date = base_date.date()
    end_date = base_date.date() - timedelta(days=1)

    response = client.get(
        f'/metrics/average_temp/{inverter.id}', params={'start_date': start_date, 'end_date': end_date}
    )

    assert response.status_code == HTTPStatus.UNPROCESSABLE_ENTITY
    assert response.json() == {'detail': 'Start date cannot be less than the end date'}
