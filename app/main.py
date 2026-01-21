from contextlib import asynccontextmanager

from fastapi import FastAPI, status, Request
from fastapi.responses import JSONResponse

from app.db.database import Base, engine
from app.errors.categories_exceptions import CategoryParentNotFoundError, CategoryNotFoundError, CategoryParentError
from app.errors.users_exceptions import UserNotFoundError
from app.errors.items_exceptions import ItemNotFoundError, WrongCategoryNotFoundError
from app.routers.categories import router as categories_router
from app.routers.users import router as users_router
from app.routers.items import router as items_router
from app.models import *  # noqa

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
app.include_router(users_router)
app.include_router(items_router)


@app.exception_handler(CategoryNotFoundError)
async def category_not_found_exception_handler(request: Request, exc: CategoryNotFoundError):
    return JSONResponse(
        status_code=status.HTTP_404_NOT_FOUND,
        content={"detail": exc.message},
    )

@app.exception_handler(CategoryParentNotFoundError)
async def category_parent_not_found_exception_handler(request: Request, exc: CategoryParentNotFoundError):
    return JSONResponse(
        status_code=status.HTTP_400_BAD_REQUEST,
        content={"detail": exc.message},
    )

@app.exception_handler(CategoryParentError)
async def category_parent_exception_handler(request: Request, exc: CategoryParentError):
    return JSONResponse(
        status_code=status.HTTP_400_BAD_REQUEST,
        content={"detail": exc.message},
    )

@app.exception_handler(UserNotFoundError)
async def user_not_found_exception_handler(request: Request, exc: UserNotFoundError):
    return JSONResponse(
        status_code=status.HTTP_404_NOT_FOUND,
        content={"detail": exc.message},
    )

@app.exception_handler(ItemNotFoundError)
async def item_not_found_exception_handler(request: Request, exc: ItemNotFoundError):
    return JSONResponse(
        status_code=status.HTTP_404_NOT_FOUND,
        content={"detail": exc.message},
    )


@app.exception_handler(WrongCategoryNotFoundError)
async def wring_category_id_exception_handler(request: Request, exc: WrongCategoryNotFoundError):
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_CONTENT,
        content={"detail": exc.message},
    )



# if __name__ == "__main__":
#     import uvicorn
#     uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)