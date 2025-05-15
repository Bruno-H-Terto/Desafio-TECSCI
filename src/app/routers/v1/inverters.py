from http import HTTPStatus
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select

from app.models import Inverter
from app.schemas import InverterList, InverterPublic, InverterSchema
from config.database import Session, get_session

router = APIRouter(prefix='/inverters', tags=['inverters'])
T_Session = Annotated[Session, Depends(get_session)]


@router.post('/', status_code=HTTPStatus.CREATED, response_model=InverterPublic)
def create_inverter(inverter: InverterSchema, session: T_Session):
    db_inverter = Inverter(plant_id=inverter.plant_id)

    session.add(db_inverter)
    session.commit()
    session.refresh(db_inverter)

    return db_inverter


@router.get('/', response_model=InverterList)
def index_inverters(session: T_Session, limit: int = 5, offset: int = 0, plant_id: int = None):
    query = select(Inverter).limit(limit).offset(offset)

    if plant_id:
        query = query.where(Inverter.plant_id == plant_id)

    inverters = session.scalars(query).all()

    return {'inverters': inverters}


@router.get('/{inverter_id}', response_model=InverterPublic)
def show_inverter(inverter_id: int, session: T_Session):
    inverter = session.scalar(select(Inverter).where(Inverter.id == inverter_id))
    if not inverter:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail='Inverter not found')
    return inverter


@router.put('/{inverter_id}', response_model=InverterPublic)
def update_inverter(inverter_id: int, inverter_data: InverterSchema, session: T_Session):
    inverter = session.scalar(select(Inverter).where(Inverter.id == inverter_id))

    if not inverter:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail='Inverter not found')

    inverter.plant_id = inverter_data.plant_id

    session.commit()
    session.refresh(inverter)

    return inverter


@router.delete('/{inverter_id}')
def delete_inverter(session: T_Session, inverter_id: int):
    inverter = session.scalar(select(Inverter).where(Inverter.id == inverter_id))

    if not inverter:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail='Inverter not found')

    session.delete(inverter)

    return {'message': 'Inverter deleted'}
