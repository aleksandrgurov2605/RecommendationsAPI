from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.db.database import Base, engine
from app.routers.categories import router as categories_router
from app.models import *

@asynccontextmanager
async def lifespan(app: FastAPI):
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    yield

    await engine.dispose()


app = FastAPI(lifespan=lifespan)


@app.get('/')
async def root():
    return {'message': 'Hello World'}


app.include_router(categories_router)
