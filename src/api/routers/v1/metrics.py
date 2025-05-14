from datetime import datetime
from http import HTTPStatus
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy import select

from api.models import Metric
from api.schemas import MetricPowerList
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

    inverter_data = session.scalars(select(Metric).where(Metric.datetime.between(start_datetime, end_datetime))).all()

    return {
        'inverter_id': inverter_id,
        'metrics': [{'date': metric.datetime.date(), 'power': metric.power} for metric in inverter_data],
    }
