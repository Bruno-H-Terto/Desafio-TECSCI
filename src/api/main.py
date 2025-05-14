from fastapi import FastAPI

from api.routers.v1 import plants

app = FastAPI()

app.include_router(plants.router)


@app.get('/')
def root():
    return {'Hello': 'World'}
