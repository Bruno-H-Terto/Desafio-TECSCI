from datetime import datetime
from http import HTTPStatus
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy import func

from api.models import Metric
from api.schemas import MetricPowerList, MetricPowerPlant, MetricTempList
from api.services.utils import TimeSeriesValue, calc_inverters_generation
from config.database import Session, get_session

PLANT_INVERTERS = {1: [1, 2, 3, 4], 2: [5, 6, 7, 8]}

router = APIRouter(prefix='/metrics', tags=['metrics'])
T_Session = Annotated[Session, Depends(get_session)]


@router.get('/max_power/{inverter_id}', response_model=MetricPowerList)
def get_max_power(
    session: T_Session,
    inverter_id: int,
    start_date: Annotated[datetime, Query(..., alias='start_date')],
    end_date: Annotated[datetime, Query(..., alias='end_date')],
):
    if start_date > end_date:
        raise HTTPException(
            status_code=HTTPStatus.UNPROCESSABLE_ENTITY, detail='Start date cannot be less than the end date'
        )

    start_datetime = datetime.combine(start_date, datetime.min.time())
    end_datetime = datetime.combine(end_date, datetime.max.time())

    inverter_data = (
        session.query(func.date(Metric.datetime).label('date'), func.max(Metric.power).label('power'))
        .filter(Metric.datetime.between(start_datetime, end_datetime))
        .group_by(func.date(Metric.datetime))
        .all()
    )

    return {
        'inverter_id': inverter_id,
        'metrics': [{'date': metric[0], 'power': metric[1]} for metric in inverter_data],
    }


@router.get('/average_temp/{inverter_id}', response_model=MetricTempList)
def get_average_temp(
    session: T_Session,
    inverter_id: int,
    start_date: Annotated[datetime, Query(..., alias='start_date')],
    end_date: Annotated[datetime, Query(..., alias='end_date')],
):
    if start_date > end_date:
        raise HTTPException(
            status_code=HTTPStatus.UNPROCESSABLE_ENTITY, detail='Start date cannot be less than the end date'
        )

    start_datetime = datetime.combine(start_date, datetime.min.time())
    end_datetime = datetime.combine(end_date, datetime.max.time())

    inverter_data = (
        session.query(func.date(Metric.datetime).label('date'), func.avg(Metric.temp_celsius).label('temp_celsius'))
        .filter(Metric.datetime.between(start_datetime, end_datetime))
        .group_by(func.date(Metric.datetime))
        .all()
    )

    return {
        'inverter_id': inverter_id,
        'metrics': [{'date': metric[0], 'temp_celsius': metric[1]} for metric in inverter_data],
    }


@router.get('/power_by_plant/{plant_id}', response_model=MetricPowerPlant)
def get_power_by_plant(
    session: T_Session,
    plant_id: int,
    start_date: Annotated[datetime, Query(..., alias='start_date')],
    end_date: Annotated[datetime, Query(..., alias='end_date')],
):
    if start_date > end_date:
        raise HTTPException(
            status_code=HTTPStatus.UNPROCESSABLE_ENTITY, detail='Start date cannot be less than the end date'
        )

    if plant_id not in PLANT_INVERTERS:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail='Plant not found')

    inverter_ids = PLANT_INVERTERS[plant_id]

    start_datetime = datetime.combine(start_date, datetime.min.time())
    end_datetime = datetime.combine(end_date, datetime.max.time())

    inverter_data = (
        session.query(Metric.datetime, Metric.power)
        .filter(Metric.datetime.between(start_datetime, end_datetime), Metric.inverter_id.in_(inverter_ids))
        .order_by(Metric.datetime)
        .all()
    )

    class _PowerEntity:
        def __init__(self, power: list[TimeSeriesValue]):
            self.power = power

    power_values = [TimeSeriesValue(value=metric.power, date=metric.datetime) for metric in inverter_data]

    total_generation = calc_inverters_generation([_PowerEntity(power=power_values)])

    return {
        'plant_id': plant_id,
        'total_generation': total_generation,
    }
