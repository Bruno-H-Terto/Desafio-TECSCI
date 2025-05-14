from fastapi import FastAPI

from api.routers.v1 import inverters, metrics, plants

app = FastAPI()

app.include_router(plants.router)
app.include_router(inverters.router)
app.include_router(metrics.router)


@app.get('/')
def root():
    return {'Hello': 'World'}
