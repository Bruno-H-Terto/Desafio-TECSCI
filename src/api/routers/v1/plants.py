from http import HTTPStatus

from fastapi import APIRouter, Depends

from api.models import Plant
from api.schemas import PlantPublic, PlantSchema
from config.database import get_session

router = APIRouter()

router = APIRouter(prefix='/plants', tags=['plants'])


@router.post('/', status_code=HTTPStatus.CREATED, response_model=PlantPublic)
def create_plant(plant: PlantSchema, session=Depends(get_session)):
    db_plant = Plant(plant_name=plant.plant_name)

    session.add(db_plant)
    session.commit()
    session.refresh(db_plant)

    return db_plant
