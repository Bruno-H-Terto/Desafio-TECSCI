from datetime import datetime
from http import HTTPStatus
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy import func

from api.models import Metric
from api.schemas import MetricPowerList, MetricTempList
from config.database import Session, get_session

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
