from pydantic import BaseModel


class PlantSchema(BaseModel):
    plant_name: str


class PlantPublic(BaseModel):
    id: int
    plant_name: str
