from http import HTTPStatus
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select

from app.models import Plant
from app.schemas import PlantList, PlantPublic, PlantSchema
from config.database import Session, get_session

router = APIRouter(prefix='/plants', tags=['plants'])
T_Session = Annotated[Session, Depends(get_session)]


@router.post('/', status_code=HTTPStatus.CREATED, response_model=PlantPublic)
def create_plant(plant: PlantSchema, session: T_Session):
    db_plant = Plant(plant_name=plant.plant_name)

    session.add(db_plant)
    session.commit()
    session.refresh(db_plant)

    return db_plant


@router.get('/', response_model=PlantList)
def index(session: T_Session, limit: int = 5, offset: int = 0):
    plants = session.scalars(select(Plant).limit(limit).offset(offset)).all()
    return {'plants': plants}


@router.get('/{plant_id}', response_model=PlantPublic)
def show_plant(plant_id: int, session: T_Session):
    plant = session.scalar(select(Plant).where(Plant.id == plant_id))
    if not plant:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail='Plant not found')
    return plant


@router.put('/{plant_id}', response_model=PlantPublic)
def update_plant(plant_id: int, plant_data: PlantSchema, session: T_Session):
    plant = session.scalar(select(Plant).where(Plant.id == plant_id))

    if not plant:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail='Plant not found')

    if plant_data.plant_name:
        existing = session.scalar(select(Plant).where(Plant.plant_name == plant_data.plant_name, Plant.id != plant_id))
        if existing:
            raise HTTPException(status_code=HTTPStatus.FORBIDDEN, detail='plant_name already in use')

    plant.plant_name = plant_data.plant_name

    session.commit()
    session.refresh(plant)

    return plant


@router.delete('/{plant_id}')
def delete_plant(session: T_Session, plant_id: int):
    plant = session.scalar(select(Plant).where(Plant.id == plant_id))

    if not plant:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail='Plant not found')

    session.delete(plant)

    return {'message': 'Plant deleted'}
