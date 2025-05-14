from http import HTTPStatus

from fastapi import APIRouter, Depends
from sqlalchemy import select

from api.models import Plant
from api.schemas import PlantList, PlantPublic, PlantSchema
from config.database import get_session

router = APIRouter(prefix='/plants', tags=['plants'])


@router.post('/', status_code=HTTPStatus.CREATED, response_model=PlantPublic)
def create_plant(plant: PlantSchema, session=Depends(get_session)):
    db_plant = Plant(plant_name=plant.plant_name)

    session.add(db_plant)
    session.commit()
    session.refresh(db_plant)

    return db_plant


@router.get('/', response_model=PlantList)
def index(session=Depends(get_session), limit=5, offset=0):
    plants = session.scalars(select(Plant).limit(limit).offset(offset))
    print(plants)

    return {'plants': plants}
