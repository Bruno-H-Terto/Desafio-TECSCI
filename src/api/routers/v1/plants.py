from fastapi import APIRouter

router = APIRouter()

router = APIRouter(prefix='/plants', tags=['plants'])


@router.post('/')
def create_plant(): ...
