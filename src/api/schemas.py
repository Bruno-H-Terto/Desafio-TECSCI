from pydantic import BaseModel, validator


class PlantSchema(BaseModel):
    plant_name: str

    @validator('plant_name')
    def name_must_not_be_empty(cls, v):
        if not v.strip():
            raise ValueError('plant_name cannot be blank')
        return v


class PlantPublic(BaseModel):
    id: int
    plant_name: str

    class Config:
        from_attributes = True


class PlantList(BaseModel):
    plants: list[PlantPublic]
